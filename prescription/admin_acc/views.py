from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema

from utils.pagination import PaginationList
from utils.renderers import UserRenderers
from utils.permissions import IsAdmin

from admin_account.project.views import AdminProjectsSerializer



from prescription.models import Prescriptions, PrescriptionContractor
from prescription.customer.serializers import CustomerPrescriptionsSerializers
from prescription.admin_acc.serializers import AdminPrescriptionSerializers, AdminPrescriptionsUserSerializer
from prescription.constractor_app.serializers import ConstractorPrescriptionsSerializer, ConstractorPrescriptionsUpddateSerializer


class AdminPrescriptionsView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]
    pagination_class = PaginationList

    @swagger_auto_schema(
        tags=['Prescription Admin'],
        responses={200: AdminPrescriptionsUserSerializer(many=True)}
    )
    def get(self, request):
        instance = PrescriptionContractor.objects.all().order_by('-id')
        # Pagination logic
        paginator = self.pagination_class()
        paginated_instances = paginator.paginate_queryset(instance, request)
        serializer = AdminPrescriptionsUserSerializer(paginated_instances, many=True, context={'request':request})
        return paginator.get_paginated_response(serializer.data)


class AdminPrescriptionView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]

    @swagger_auto_schema(
        tags=['Prescription Admin'],
        responses={200: AdminPrescriptionsUserSerializer(many=False)},
    )
    def get(self, request, pk):
        instances = get_object_or_404(PrescriptionContractor, id=pk)
        serializer = AdminPrescriptionsUserSerializer(instances, context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        tags=['Prescription Admin'],
        request_body=AdminPrescriptionSerializers
    )
    def put(self, request, pk):
        instance = PrescriptionContractor.objects.filter(id=pk)[0]
        # Make sure to check that data is not a list, but a dictionary
        serializer = AdminPrescriptionSerializers(instance=instance, data=request.data, context={'owner':request.user, 'request': request}, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
