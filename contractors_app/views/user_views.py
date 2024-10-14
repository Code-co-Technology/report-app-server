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
from utils.permissions import IsContractors

from authen.models import CustomUser
from contractors_app.serializers.user_serializers import ContractorGorupsUserSerializer, ContractorAddUserSerializer, ContractorUsersSerializer, ContractorUserSerializer


""" All functions for managing users for the Contractor Role """

class ContractorUserGroupView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsContractors]

    @swagger_auto_schema(
        tags=['Contractor Account'],
        responses={200: ContractorGorupsUserSerializer(many=True)},
        operation_summary='All roles are for Contractor',
        operation_description='All roles are for Contractor.'
    )
    def get(self, request):
        group = Group.objects.filter(groups__name__in=['user'])
        serializer = ContractorGorupsUserSerializer(group, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ContractorUsersView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsContractors]
    pagination_class = PaginationList

    @swagger_auto_schema(
        tags=['Contractor Account'],
        manual_parameters=[
            openapi.Parameter('q', openapi.IN_QUERY, description='Search query for filtering by First Name, Last Name, Email fields', type=openapi.TYPE_STRING),
            openapi.Parameter('activate_profile', openapi.IN_QUERY, description='Filter by active profile status (true/false)', type=openapi.TYPE_BOOLEAN),
        ],
        responses={200: ContractorUsersSerializer(many=True)},
        operation_summary='Contractor all users',
        operation_description='Contractor employees arrive. Filters can be applied based on search query, active profile status, and user role.'
    )
    def get(self, request):
        instances = CustomUser.objects.filter(company=request.user.company, groups__name__in=['contractors', 'user']).order_by('-id')
        filters = Q()

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
        serializer = ContractorUsersSerializer(paginated_instances, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)

    @swagger_auto_schema(
        tags=['Contractor Account'],
        request_body=ContractorAddUserSerializer,
        operation_summary='Add a Contractor employee.',
        operation_description='Contractor can add employee to your company.'
    )
    def post(self, request):
        serializer = ContractorAddUserSerializer(data=request.data, request={'company':request.user.company})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Вы зарегистрировались. Подождите, пока ваш профиль будет одобрен администратором.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContractorUserView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsContractors]

    @swagger_auto_schema(
        tags=['Contractor Account'],
        responses={200: ContractorUsersSerializer(many=False)},
        operation_summary='Contractor get by user id',
        operation_description='Contractor get by user id'
    )
    def get(self, request, pk):
        instance = get_object_or_404(CustomUser, company=request.user.company, id=pk)
        serializer = ContractorUsersSerializer(instance, context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        tags=['Contractor Account'],
        request_body=ContractorUserSerializer,
        operation_summary='Contractor put by user id',
        operation_description='This last point can change the information about your employees. Contractor only.'
    )
    def put(self, request, pk):
        queryset = get_object_or_404(CustomUser, company=request.user.company, id=pk)
        serializer = ContractorUserSerializer(context={'request': request}, instance=queryset, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        tags=['Contractor Account'],
        responses={204:  'No Content'},
        operation_summary='Contractor deleted by user id',
        operation_description='A Contractor can only delete his own employee.'
    )
    def delete(self, request, pk):
        user_delet = get_object_or_404(CustomUser, company=request.user.company, id=pk)
        user_delet.delete()
        return Response({"message": "Пользователь удален"}, status=status.HTTP_204_NO_CONTENT)