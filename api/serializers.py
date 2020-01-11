from rest_framework.serializers import ModelSerializer
from rest_framework.authtoken.models import Token


from django.contrib.auth.models import User
from sender.models import EmailObject
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

