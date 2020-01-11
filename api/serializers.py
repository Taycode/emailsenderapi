from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework.authtoken.models import Token
from rest_framework import serializers


from django.contrib.auth.models import User
from sender.models import EmailObject
from .tasks import sender_func
from django.contrib.auth import authenticate


class UserCreateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):

        user = User(
            username=validated_data['username'].lower(),
            email=validated_data['email'].lower(),
        )
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user


class LoginSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'password']


class EmailObjectSerializer(ModelSerializer):
    class Meta:
        model = EmailObject
        fields = '__all__'


class SendEmailSerializer(Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    @staticmethod
    def send(validated_data, **kwargs):
        email_object = EmailObject.objects.get(pk=kwargs['email_object_id'])
        path = [paths.file.path for paths in email_object.attachments.all()]
        file = open('log.txt', 'a')
        for recipient in email_object.recipient.all():
            sender_func.delay(
                email=validated_data['email'],
                password=validated_data['password'],
                recipient=recipient.email,
                subject=email_object.subject,
                body=email_object.body,
                path=path
            )

            file.write('email sent to {}\n'.format(recipient.email))
        file.close()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

