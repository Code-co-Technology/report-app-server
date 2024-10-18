from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from utils.pagination import PaginationList
from utils.renderers import UserRenderers
from utils.permissions import IsCustomer

from admin_account.models import Project
from admin_account.project import AdminProjectsSerializer

from prescription.models import TypeOfViolation, Prescriptions
from prescription.customer.serializers import TypeOFViolationSerializer, CustomerPrescriptionsSerializers


class CustomerProjectView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsCustomer]

    @swagger_auto_schema(
        tags=['Prescription Customer'],
        responses={200: AdminProjectsSerializer(many=True)},
        operation_summary='For Customer Projects'
    )
    def get(self, request):
        instance = Project.objects.filter(status=False).order_by('-id')
        serializer = AdminProjectsSerializer(instance, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class CustomerTypeOfViolationView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsCustomer]

    @swagger_auto_schema(
        tags=['Prescription Customer'],
        responses={200: TypeOFViolationSerializer(many=True)}
    )
    def get(self, request):
        instance = TypeOfViolation.objects.all().order_by('-id')
        serializer = TypeOFViolationSerializer(instance, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class UstumerPrescriptionsView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsCustomer]
    pagination_class = PaginationList

    @swagger_auto_schema(
        tags=['Prescription Customer'],
        responses={200: CustomerPrescriptionsSerializers(many=True)}
    )
    def get(self, request):
        instance = Prescriptions.objects.filter().order_by('-id')
        # Pagination logic
        paginator = self.pagination_class()
        paginated_instances = paginator.paginate_queryset(instance, request)
        serializer = CustomerPrescriptionsSerializers(paginated_instances, many=True, context={'request':request})
        return paginator.get_paginated_response(serializer.data)
