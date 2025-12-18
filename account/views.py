from locale import setlocale

from django.core.serializers import serialize
from django.shortcuts import render
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_205_RESET_CONTENT, HTTP_406_NOT_ACCEPTABLE
from rest_framework.views import APIView

from account.models import Service
from account.serializers import CreateUserSerializer, ActivateUserSerializer, LoginUserSerializer, UpdateUserSerializer, \
    ConfirmedUpdateUserEmailSerializer, ConfirmUpdateUserPasswordSerializer


class CreateUserView(APIView):
    def post(self, request):
        data = request.data
        serializer = CreateUserSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.create(serializer.validated_data)
            user.send_activation_code()
            return Response(user.get_info(), status=status.HTTP_201_CREATED)



class ActivateUserView(APIView):
    def post(self, request):
        data = request.data
        serializer = ActivateUserSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.activate(serializer.validated_data)
            if user:
                return Response(user.get_info(), status=HTTP_205_RESET_CONTENT)
            return Response('activation code is wrong', status=HTTP_406_NOT_ACCEPTABLE)



class LoginUserView(ObtainAuthToken):
    serializer_class = LoginUserSerializer
    response = Response

class LogoutUserView(APIView):
    permission_classes = [IsAuthenticated, ]

    def delete(self, request):
        user = request.user

        try:
            token = Token.objects.get(user=user)
            token.delete()
            return Response('user was successfully logged out', status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response ('user was not logged out', status=status.HTTP_406_NOT_ACCEPTABLE)

class UpdateUserView(APIView):
    permission_classes = [IsAuthenticated, ]

    def patch(self, request):
        user = request.user
        data = request.data

        serializer = UpdateUserSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.update(user, serializer.validated_data)
            return Response(user.get_info(), status=status.HTTP_200_OK)


class UpdateUserEmailView(APIView):
    permission_classes = [IsAuthenticated, ]

    def patch(self, request):
        user = request.user
        user.activation_code = Service.generate_activation_code(6)
        user.save()
        user.send_activation_code()
        return Response('check your email, habibi', status=status.HTTP_200_OK)


class ConfirmedUpdateUserEmailView(APIView):
    permission_classes = [IsAuthenticated, ]

    def patch(self, request):
        user = request.user
        data = request.data

        serializer = ConfirmedUpdateUserEmailSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.update(user, serializer.validated_data)
            if user:
                return Response(user.get_info(), status=status.HTTP_200_OK)
            return Response('email was not updated', status=status.HTTP_406_NOT_ACCEPTABLE)


class UpdateUserPasswordView(APIView):
    permission_classes = [IsAuthenticated, ]

    def patch(self, request):
        user = request.user
        user.activation_code = Service.generate_activation_code(6)
        user.save()
        user.send_activation_code()
        return Response ('check email', status=status.HTTP_200_OK)


class ConfirmUpdateUserPasswordView(APIView):
    permission_classes = [IsAuthenticated, ]

    def patch(self, request):
        user = request.user
        data = request.data
        serializer = ConfirmUpdateUserPasswordSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.update(user, serializer.validated_data)
            if user:
                return Response('password was successfully changed', status=status.HTTP_200_OK)
            return Response('something went wrong', status=status.HTTP_418_IM_A_TEAPOT)

