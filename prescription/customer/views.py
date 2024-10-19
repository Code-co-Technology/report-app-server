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
from admin_account.project.views import AdminProjectsSerializer

from prescription.models import TypeOfViolation, Prescriptions
from prescription.customer.serializers import TypeOFViolationSerializer, CustomerPrescriptionsSerializers, CustomerPrescriptionSerializers


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
        instance = Prescriptions.objects.filter(owner=request.user).order_by('-id')
        # Pagination logic
        paginator = self.pagination_class()
        paginated_instances = paginator.paginate_queryset(instance, request)
        serializer = CustomerPrescriptionsSerializers(paginated_instances, many=True, context={'request':request})
        return paginator.get_paginated_response(serializer.data)

    @swagger_auto_schema(
        tags=['Prescription Customer'],
        request_body=CustomerPrescriptionSerializers,
        operation_summary='Submit a prescription.'
    )
    def post(self, request):
        serializer = CustomerPrescriptionSerializers(data=request.data, context={'owner':request.user, 'request':request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)