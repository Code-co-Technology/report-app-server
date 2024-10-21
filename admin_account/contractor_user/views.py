from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema

from utils.pagination import PaginationList
from utils.renderers import UserRenderers
from utils.permissions import IsAdmin

from authen.models import CustomUser, Overdue, FailedReports
from admin_account.contractor_user.serializers import AdminOverdueSerializer, AdminFailedReportsSerializer, AdminContractorUserSerializer, AdminContractorUserUpdateSerializer


class AdminContraCountUsersView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]
    pagination_class = PaginationList

    @swagger_auto_schema(
        tags=['Admin Account Custumer User'],
        responses={200: AdminContractorUserSerializer(many=True)},
    )
    def get(self, request):
        instances = CustomUser.objects.filter(activate_profile=False, groups__name__in=['contractors']).count()
        return Response(instances, status=status.HTTP_200_OK)


class AdminOverdueView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]

    @swagger_auto_schema(
        tags=['Admin Account Contractor User'],
        responses={200: AdminOverdueSerializer(many=True)},
        operation_description='Overdue for Contractor. For Admin role only'
    )
    def get(self, request):
        instances = Overdue.objects.all().order_by('id')
        serializer = AdminOverdueSerializer(instances, many=True, context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class AdminFailedReportsView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]

    @swagger_auto_schema(
        tags=['Admin Account Contractor User'],
        responses={200: AdminFailedReportsSerializer(many=True)},
        operation_description='Failed Reports for Contractor. For Admin role only'
    )
    def get(self, request):
        instances = FailedReports.objects.all().order_by('id')
        serializer = AdminFailedReportsSerializer(instances, many=True, context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class AdminContractorFalseUsersView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]
    pagination_class = PaginationList

    @swagger_auto_schema(
        tags=['Admin Account Contractor User'],
        responses={200: AdminContractorUserSerializer(many=True)},
        operation_summary='Newly registered and Inactive',
        operation_description='Contractor is all non-Active users. For admin role only. For admin role only'
    )
    def get(self, request):
        instances = CustomUser.objects.filter(activate_profile=False, groups__name__in=['contractors']).order_by('-id')
        # Pagination logic
        paginator = self.pagination_class()
        paginated_instances = paginator.paginate_queryset(instances, request)
        serializer = AdminContractorUserSerializer(paginated_instances, many=True, context={'request':request})
        return paginator.get_paginated_response(serializer.data)


class AdminContractorUsersView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]
    pagination_class = PaginationList

    @swagger_auto_schema(
        tags=['Admin Account Contractor User'],
        responses={200: AdminContractorUserSerializer(many=True)},
        operation_summary='Those who are active',
        operation_description='Contractor are all Active users. For Admin role only'
    )
    def get(self, request):
        instances = CustomUser.objects.filter(activate_profile=True, groups__name__in=['contractors']).order_by('-id')
        # Pagination logic
        paginator = self.pagination_class()
        paginated_instances = paginator.paginate_queryset(instances, request)
        serializer = AdminContractorUserSerializer(paginated_instances, many=True, context={'request':request})
        return paginator.get_paginated_response(serializer.data)


class AdminContractorUserView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]

    @swagger_auto_schema(
        tags=['Admin Account Contractor User'],
        responses={200: AdminContractorUserSerializer(many=False)},
        operation_description='Contractors get by id users. For Admin role only'
    )
    def get(self, request, pk):
        instances = get_object_or_404(CustomUser, id=pk)
        serializer = AdminContractorUserSerializer(instances, context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        tags=['Admin Account Contractor User'],
        request_body=AdminContractorUserUpdateSerializer,
        operation_description='This last point can change the information about your user. Admin only.'
    )
    def put(self, request, pk):
        instance = get_object_or_404(CustomUser, id=pk)
        # Make sure to check that data is not a list, but a dictionary
        serializer = AdminContractorUserUpdateSerializer(instance=instance, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)