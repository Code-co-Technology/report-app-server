from rest_framework import status, generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action

from django.shortcuts import get_object_or_404
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import authenticate
from django.contrib.auth import update_session_auth_hash
from django.utils.encoding import smart_bytes
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from utils.renderers import UserRenderers
from utils.permissions import IsLogin, IsAdmin
from utils.utils import Util

from authen.models import CustomUser, Company
from authen.serializers import (
    UserGroupSerizliers,
    UserSignUpSerializer,
    UserSigInSerializer,
    UserInformationSerializer,
)


def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {"refresh": str(refresh), "access": str(refresh.access_token)}


class UserGroupView(APIView):

    @swagger_auto_schema(tags=["Auth"], responses={200: UserGroupSerizliers(many=True)})
    def get(self, request):
        group = Group.objects.all()
        serializer = UserGroupSerizliers(group, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserSignUp(APIView):
    render_classes = [UserRenderers]

    @swagger_auto_schema(tags=["Auth"], request_body=UserSignUpSerializer)
    def post(self, request):
        serializer = UserSignUpSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            instanse = serializer.save()
            return Response({'message': 'Вы зарегистрировались. Подождите, пока ваш профиль будет одобрен администратором. На ваш адрес электронной почты будет отправлено сообщение.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserSignIn(APIView):
    render_classes = [UserRenderers]

    @swagger_auto_schema(tags=["Auth"], request_body=UserSigInSerializer)
    def post(self, request):
        serializer = UserSigInSerializer(data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            email = request.data["email"]
            password = request.data["password"]
            user = authenticate(email=email, password=password)
            
            if user is not None:
                # Tekshiruv: Agar profil faollashtirilmagan bo'lsa
                if not user.activate_profile:
                    return Response(
                        {'error': 'Ваш профиль еще не активирован. Пожалуйста, свяжитесь с администратором.'},
                        status=status.HTTP_403_FORBIDDEN
                    )
                
                # Agar foydalanuvchi faollashtirilgan bo'lsa token yaratish
                tokens = get_token_for_user(user)
                return Response(tokens, status=status.HTTP_200_OK)
            else:
                return Response(
                    {'error': "Этот пользователь недоступен для системы"}, 
                    status=status.HTTP_404_NOT_FOUND
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfile(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsLogin]

    @swagger_auto_schema(tags=["Auth"], responses={200: UserInformationSerializer(many=True)})
    def get(self, request):
        serializer = UserInformationSerializer(request.user, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
