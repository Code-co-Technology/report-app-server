from rest_framework import status, generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action

from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import authenticate
from django.contrib.auth import update_session_auth_hash
from django.utils.encoding import smart_bytes
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate
from django.core.mail import send_mail

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from utils.pagination import PaginationList
from utils.renderers import UserRenderers
from utils.permissions import IsCustomer
from utils.utils import Util

from authen.models import CustomUser
from customer_account.serializers import CustomerGorupsUserSerializer, CustumerAddUserSerializer, CustomUsersSerializer



""" All functions for managing users for the Customers Role """


class CustumerUserGroupView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsCustomer]

    @swagger_auto_schema(
        tags=['Custumer Account'],
        responses={200: CustomerGorupsUserSerializer(many=True)},
        operation_summary='All roles are for Custumer',
        operation_description='All roles are for Custumer.'
    )
    def get(self, request):
        group = Group.objects.filter(groups__name__in=['contractors', 'user'])
        serializer = CustomerGorupsUserSerializer(group, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CustumerUsersView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsCustomer]
    pagination_class = PaginationList

    @swagger_auto_schema(
        tags=['Custumer Account'],
        manual_parameters=[
            openapi.Parameter('q', openapi.IN_QUERY, description='Search query for filtering by First Name, Last Name, Email fields', type=openapi.TYPE_STRING),
            openapi.Parameter('activate_profile', openapi.IN_QUERY, description='Filter by active profile status (true/false)', type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('groups', openapi.IN_QUERY, description='Filter by user role. Roll id will be given', type=openapi.TYPE_INTEGER),
        ],
        responses={200: CustomUsersSerializer(many=True)},
        operation_summary='Custumers all users',
        operation_description='Custumers all users except the custumer role. Filters can be applied based on search query, active profile status, and user role.'
    )
    def get(self, request):
        instances = CustomUser.objects.filter(company=request.user.company, groups__name__in=['contractors', 'user']).order_by('-id')
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
                Q(last_name__icontains=search_query)
            )
        instances = instances.filter(filters)

        # Pagination logic
        paginator = self.pagination_class()
        paginated_instances = paginator.paginate_queryset(instances, request)
        serializer = CustomUsersSerializer(paginated_instances, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)