from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response

from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group
from django.core.mail import send_mail

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from utils.pagination import PaginationList
from utils.renderers import UserRenderers
from utils.permissions import IsAdmin

from authen.models import CustomUser
from admin_account.serializers.users_serializers import UsersSerializer, ActivateUserSerializer, UsersGroupSerizliers

""" All functions for managing users for the Admin Role """

class UserGroupView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]

    @swagger_auto_schema(
        tags=['Admin Account'],
        responses={200: UsersSerializer(many=True)},
        operation_summary='All roles are for Admin',
        operation_description='All roles are for Admin.'
    )
    def get(self, request):
        group = Group.objects.filter(groups__name__in=['contractors', 'customer', 'user'])
        serializer = UsersGroupSerizliers(group, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UsersView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]
    pagination_class = PaginationList

    @swagger_auto_schema(
        tags=['Admin Account'],
        manual_parameters=[
            openapi.Parameter('q', openapi.IN_QUERY, description='Search query for filtering by First Name, Last Name, Email, Company name fields', type=openapi.TYPE_STRING),
            openapi.Parameter('activate_profile', openapi.IN_QUERY, description='Filter by active profile status (true/false)', type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('groups', openapi.IN_QUERY, description='Filter by user role. Roll id will be given', type=openapi.TYPE_INTEGER),
        ],
        responses={200: UsersSerializer(many=True)},
        operation_summary='All users',
        operation_description='All users except the admin role. Filters can be applied based on search query, active profile status, and user role.'
    )
    def get(self, request):
        instances = CustomUser.objects.filter(groups__name__in=['contractors', 'customer', 'user']).order_by('-id')
        filters = Q()
        # Filter by group if provided
        groups = request.query_params.get('groups')
        if groups:
            filters &= Q(groups__id=groups)

        # Filter by activate_profile if provided and it's a valid boolean
        activate_profile = request.query_params.get('activate_profile')
        if activate_profile is not None:
            activate_profile_bool = activate_profile.lower() == 'true'
            filters &= Q(activate_profile=activate_profile_bool)

        # Search query for first name, last name, email, or company name
        search_query = request.query_params.get('q')
        if search_query:
            filters &= (
                Q(email__icontains=search_query) |
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(company__name_company__icontains=search_query)
            )
        instances = instances.filter(filters)

        # Pagination logic
        paginator = self.pagination_class()
        paginated_instances = paginator.paginate_queryset(instances, request)
        serializer = UsersSerializer(paginated_instances, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)


class UserNoActiveView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]
    pagination_class = PaginationList

    @swagger_auto_schema(
        tags=['Admin Account'],
        responses={200: UsersSerializer(many=True)},
        operation_summary='New users who are not active',
        operation_description='Lists all inactive users.'
    )
    def get(self, request):
        users = CustomUser.objects.filter(activate_profile=False, groups__name__in=['contractors', 'customer', 'user']).order_by('-id')
        # Pagination logic
        paginator = self.pagination_class()
        paginated_instances = paginator.paginate_queryset(users, request)
        serializer = UsersSerializer(paginated_instances, many=True, context={'request':request})
        return paginator.get_paginated_response(serializer.data)


class ActivateUsersView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]

    @swagger_auto_schema(
        tags=['Admin Account'],
        responses={200: UsersSerializer(many=False)},
        operation_summary='Get user details by ID',
        operation_description='This endpoint retrieves the details of a user based on their unique ID. Admins can access this information to manage user accounts.'
    )
    def get(self, request, pk):
        users = get_object_or_404(CustomUser, id=pk)
        serializer = UsersSerializer(users, context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)


    @swagger_auto_schema(
        tags=['Admin Account'],
        request_body=ActivateUserSerializer,
        operation_summary='Activate or deactivate a user account',
        operation_description='This endpoint allows an admin to activate or deactivate a user account by updating the user\'s status.'
    )
    def patch(self, request, pk):
        queryset = get_object_or_404(CustomUser, id=pk)
        serializer = ActivateUserSerializer(context={'request': request}, instance=queryset, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            if user.activate_profile:
                send_mail(
                    subject='Аккаунт активирован',
                    message='Ваша учетная запись успешно активирована.',
                    from_email='your_email@example.com',
                    recipient_list=[user.email],
                    fail_silently=False,
                )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
