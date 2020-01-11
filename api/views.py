from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from .serializers import UserCreateSerializer, LoginSerializer, EmailObjectSerializer, SendEmailSerializer

from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class RegisterView(APIView):
    serializer_class = UserCreateSerializer
    permission_classes = ()
    authentication_classes = ()

    @staticmethod
    def post(request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    serializer_class = LoginSerializer

    @staticmethod
    def post(request):
        email = request.data['email']
        password = request.data['password']
        try:
            user = User.objects.get(email=email)
            user = authenticate(username=user.username, password=password)
            if user is not None:
                data = {'Token': user.auth_token.key}
                return Response(data, status=status.HTTP_200_OK)
            else:
                data = {'error': 'Wrong credentials'}
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            data = {'error': 'User does not exist'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class EmailObjectCreate(APIView):
    serializer_class = EmailObjectSerializer

    @staticmethod
    def post(request):
        serializer = EmailObjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendEmail(APIView):
    serializer_class = SendEmailSerializer

    @staticmethod
    def post(request, pk):
        serializer = SendEmailSerializer(data=request.data)
        if serializer.is_valid():
            print(serializer.validated_data)
            serializer.send(email_object_id=pk, validated_data=serializer.validated_data)
            data = {'status': 'success'}
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
