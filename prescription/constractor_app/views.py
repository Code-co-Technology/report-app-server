from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema

from utils.pagination import PaginationList
from utils.renderers import UserRenderers
from utils.permissions import IsContractors

from admin_account.project.views import AdminProjectsSerializer

from prescription.models import Prescriptions, PrescriptionContractor
from prescription.customer.serializers import CustomerPrescriptionsSerializers
from prescription.constractor_app.serializers import ContractorsPrescriptionSerializers, ConstractorPrescriptionsSerializer, ConstractorPrescriptionsUpddateSerializer


class ContractorsPrescriptionCountView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsContractors]

    @swagger_auto_schema(
        tags=['Prescription Contractors'],
        responses={200: CustomerPrescriptionsSerializers(many=True)}
    )
    def get(self, request):
        instance = Prescriptions.objects.filter(contractor=request.user, status=1).count()
        serializer = CustomerPrescriptionsSerializers(instance, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class ContractorsPrescriptionNewView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsContractors]

    @swagger_auto_schema(
        tags=['Prescription Contractors'],
        responses={200: CustomerPrescriptionsSerializers(many=True)}
    )
    def get(self, request):
        instance = Prescriptions.objects.filter(contractor=request.user, status=1)\
                                        .select_related('project', 'owner')\
                                        .prefetch_related('contractor', 'type_violation')\
                                        .order_by('-id')
        serializer = CustomerPrescriptionsSerializers(instance, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class ContractorsPrescriptioneliminatedView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsContractors]

    @swagger_auto_schema(
        tags=['Prescription Contractors'],
        responses={200: CustomerPrescriptionsSerializers(many=True)}
    )
    def get(self, request):
        instance = Prescriptions.objects.filter(contractor=request.user, status=2)\
                                        .select_related('project', 'owner')\
                                        .prefetch_related('type_violation')\
                                        .order_by('-id')
        # Serializing paginated data
        serializer = CustomerPrescriptionsSerializers(instance, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class ContractorsPrescriptioneExpiredView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsContractors]

    @swagger_auto_schema(
        tags=['Prescription Contractors'],
        responses={200: CustomerPrescriptionsSerializers(many=True)}
    )
    def get(self, request):
        instance = Prescriptions.objects.filter(contractor=request.user, status=3)\
                                        .select_related('project', 'owner')\
                                        .prefetch_related('type_violation')\
                                        .order_by('-id')
        # Serializing paginated data
        serializer = CustomerPrescriptionsSerializers(instance, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class ContractorsPrescriptionsView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsContractors]
    pagination_class = PaginationList

    @swagger_auto_schema(
        tags=['Prescription Contractors'],
        responses={200: ConstractorPrescriptionsSerializer(many=True)}
    )
    def get(self, request):
        instance = PrescriptionContractor.objects.filter(contractor=request.user).order_by('-id')
        # Pagination logic
        paginator = self.pagination_class()
        paginated_instances = paginator.paginate_queryset(instance, request)
        # Serializing paginated data
        serializer = ConstractorPrescriptionsSerializer(paginated_instances, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)


class ContractorsPrescriptionUserView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsContractors]

    @swagger_auto_schema(
        tags=['Prescription Contractors'],
        responses={200: ConstractorPrescriptionsSerializer(many=True)}
    )
    def get(self, request, pk):
        instance = get_object_or_404(PrescriptionContractor, id=pk)

        serializer = ConstractorPrescriptionsSerializer(instance, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        tags=['Prescription Contractors'],
        request_body=ConstractorPrescriptionsUpddateSerializer
    )
    def put(self, request, pk):
        instance = get_object_or_404(PrescriptionContractor, id=pk)
        # Make sure to check that data is not a list, but a dictionary
        serializer = ConstractorPrescriptionsUpddateSerializer(instance=instance, data=request.data, context={'owner':request.user, 'request': request}, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContractorsPrescriptionView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsContractors]

    @swagger_auto_schema(
        tags=['Prescription Contractors'],
        responses={200: CustomerPrescriptionsSerializers(many=False)},
    )
    def get(self, request, pk):
        instances = get_object_or_404(Prescriptions, id=pk)
        serializer = CustomerPrescriptionsSerializers(instances, context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=['Prescription Contractors'],
        request_body=ContractorsPrescriptionSerializers
    )
    def put(self, request, pk):
        instance = get_object_or_404(Prescriptions, id=pk)
        # Make sure to check that data is not a list, but a dictionary
        serializer = ContractorsPrescriptionSerializers(instance=instance, data=request.data, context={'owner':request.user, 'request': request}, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)