from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response

from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from utils.pagination import PaginationList
from utils.renderers import UserRenderers
from utils.permissions import IsCustomer

from authen.models import CustomUser
from customer_account.serializers.users_serializers import CustomerGorupsUserSerializer, CustumerAddUserSerializer, CustomUsersSerializer, CustomUserSerializer


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
        operation_description='Customer-related employees arrive. Filters can be applied based on search query, active profile status, and user role.'
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

    @swagger_auto_schema(
        tags=['Custumer Account'],
        request_body=CustumerAddUserSerializer,
        operation_summary='Add a customer employee.',
        operation_description='Customer can add employee to your company. \nGroups: \n1. contractors \n2. user'
    )
    def post(self, request):
        serializer = CustumerAddUserSerializer(data=request.data, request={'company':request.user.company})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Вы зарегистрировались. Подождите, пока ваш профиль будет одобрен администратором.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerUserView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsCustomer]

    @swagger_auto_schema(
        tags=['Custumer Account'],
        responses={200: CustomUsersSerializer(many=False)},
        operation_summary='Custumers get by user id',
        operation_description='Custumers get by user id'
    )
    def get(self, request, pk):
        instance = get_object_or_404(CustomUser, company=request.user.company, id=pk)
        serializer = CustomUsersSerializer(instance, context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        tags=['Custumer Account'],
        request_body=CustomUserSerializer,
        operation_summary='Custumers put by user id',
        operation_description='This last point can change the information about your employees. Customer only.'
    )
    def put(self, request, pk):
        queryset = get_object_or_404(CustomUser, company=request.user.company, id=pk)
        serializer = CustomUserSerializer(context={'request': request}, instance=queryset, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        tags=['Custumer Account'],
        responses={204:  'No Content'},
        operation_summary='Custumers deleted by user id',
        operation_description='A customer can only delete his own employee.'
    )
    def delete(self, request, pk):
        user_delet = get_object_or_404(CustomUser, company=request.user.company, id=pk)
        user_delet.delete()
        return Response({"message": "Пользователь удален"}, status=status.HTTP_204_NO_CONTENT)
