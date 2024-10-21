from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema

from utils.pagination import PaginationList
from utils.renderers import UserRenderers
from utils.permissions import IsAdmin

from authen.models import CustomUser
from admin_account.customer_user.serializers import AdminCustumerUserSerializer, AdminCustumerUserUpdateSerializer



class AdminCustumerCountUsersView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]
    pagination_class = PaginationList

    @swagger_auto_schema(
        tags=['Admin Account Custumer User'],
        responses={200: AdminCustumerUserSerializer(many=True)},
    )
    def get(self, request):
        instances = CustomUser.objects.filter(activate_profile=True, groups__name__in=['customer']).count()
        return Response(instances, status=status.HTTP_200_OK)


class AdminCustumerFalseUsersView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]
    pagination_class = PaginationList

    @swagger_auto_schema(
        tags=['Admin Account Custumer User'],
        responses={200: AdminCustumerUserSerializer(many=True)},
        operation_summary='Newly registered and Inactive',
        operation_description='Customer is all non-Active users. For admin role only. For admin role only'
    )
    def get(self, request):
        instances = CustomUser.objects.filter(activate_profile=False, groups__name__in=['customer']).order_by('-id')
        # Pagination logic
        paginator = self.pagination_class()
        paginated_instances = paginator.paginate_queryset(instances, request)
        serializer = AdminCustumerUserSerializer(paginated_instances, many=True, context={'request':request})
        return paginator.get_paginated_response(serializer.data)


class AdminCustumerUsersView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]
    pagination_class = PaginationList

    @swagger_auto_schema(
        tags=['Admin Account Custumer User'],
        responses={200: AdminCustumerUserSerializer(many=True)},
        operation_summary='Those who are active',
        operation_description='Customer are all Active users. For admin role only'
    )
    def get(self, request):
        instances = CustomUser.objects.filter(activate_profile=True, groups__name__in=['customer']).order_by('-id')
        # Pagination logic
        paginator = self.pagination_class()
        paginated_instances = paginator.paginate_queryset(instances, request)
        serializer = AdminCustumerUserSerializer(paginated_instances, many=True, context={'request':request})
        return paginator.get_paginated_response(serializer.data)


class AdminCustumerUserView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]

    @swagger_auto_schema(
        tags=['Admin Account Custumer User'],
        responses={200: AdminCustumerUserSerializer(many=False)},
        operation_description='Custumer get by id users. For Admin role only'
    )
    def get(self, request, pk):
        instances = get_object_or_404(CustomUser, id=pk)
        serializer = AdminCustumerUserSerializer(instances, context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        tags=['Admin Account Custumer User'],
        request_body=AdminCustumerUserUpdateSerializer,
        operation_description='This last point can change the information about your user. Admin only.'
    )
    def put(self, request, pk):
        instance = get_object_or_404(CustomUser, id=pk)
        # Make sure to check that data is not a list, but a dictionary
        serializer = AdminCustumerUserUpdateSerializer(instance=instance, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
