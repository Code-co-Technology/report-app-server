from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, JSONParser, FormParser

from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema

from utils.pagination import PaginationList
from utils.renderers import UserRenderers
from utils.permissions import IsAdmin

from report_app.models import ReportsName
from report_app.reports.serializers import ReportsNamesSerializer

from prescription.constractor_app.serializers import ConstractorPrescriptionsSerializer
from prescription.models import PrescriptionContractor
from admin_account.models import Project, ProjectImage, ProjectSmeta
from admin_account.project.serializers import (
    AdminProjectsSerializer, AdminCreateProjectSerializer, AdminUpdateProjectSerializer, 
    AdminProjectImagesSerializer, AdminProjectImageSerializer,
    AdminProjectFilesSerializer, AdminProjectFileSerializer
)


class AdminProjectsView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]
    pagination_class = PaginationList
    parser_classes = [MultiPartParser, FormParser, JSONParser] 

    @swagger_auto_schema(
        tags=['Admin Account Project'],
        responses={200: AdminProjectsSerializer(many=True)},
        operation_summary='All projects for admin.',
        operation_description='All projects for the admin role.'
    )
    def get(self, request):
        instances = Project.objects.all().order_by('-id')
        # Pagination logic
        paginator = self.pagination_class()
        paginated_instances = paginator.paginate_queryset(instances, request)
        serializer = AdminProjectsSerializer(paginated_instances, many=True, context={'request':request})
        return paginator.get_paginated_response(serializer.data)
    
    @swagger_auto_schema(
        tags=['Admin Account Project'],
        request_body=AdminCreateProjectSerializer,
        consumes=['application/json', 'multipart/form-data'],
        operation_summary='Create a new project.',
        operation_description='Admin adds new project. \nRequired fields: \n1. address \n2. opening_date \n3. submission_deadline')
    def post(self, request):
        serializer = AdminCreateProjectSerializer(data=request.data, context={'owner':request.user, 'request':request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminProjectPrescriptionView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]

    @swagger_auto_schema(
        tags=['Admin Account Project'],
        responses={200: ConstractorPrescriptionsSerializer(many=True)},
        operation_summary='Admin get by project id',
        operation_description='Admin get by project id'
    )
    def get(self, request, pk):
        instances = PrescriptionContractor.objects.filter(prescription__project__id=pk)
        serializer = ConstractorPrescriptionsSerializer(instances, many=True, context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class AdminProjectReportView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]

    @swagger_auto_schema(
        tags=['Admin Account Project'],
        responses={200: ReportsNamesSerializer(many=True)},
    )
    def get(self, request, pk):
        instances = ReportsName.objects.filter(project__id=pk)
        serializer = ReportsNamesSerializer(instances, many=True, context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class AdminProjectView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]

    @swagger_auto_schema(
        tags=['Admin Account Project'],
        responses={200: AdminProjectsSerializer(many=False)},
        operation_summary='Admin get by project id',
        operation_description='Admin get by project id'
    )
    def get(self, request, pk):
        instances = get_object_or_404(Project, id=pk)
        serializer = AdminProjectsSerializer(instances, context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        tags=['Admin Account Project'],
        request_body=AdminUpdateProjectSerializer,
        operation_summary='Admin put by project id',
        operation_description='This last point can change the information about your project. Admin only.'
    )
    def put(self, request, pk):
        instance = get_object_or_404(Project, id=pk)
        # Make sure to check that data is not a list, but a dictionary
        serializer = AdminUpdateProjectSerializer(instance=instance, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        tags=['Admin Account Project'],
        responses={204:  'No Content'},
        operation_summary='Admin deleted by project id',
        operation_description='A Admin can only delete his own project.'
    )
    def delete(self, request, pk):
        project_delete = get_object_or_404(Project, id=pk)
        project_delete.delete()
        return Response({"message": "Проект удален"}, status=status.HTTP_204_NO_CONTENT)
    

class ProjectImageView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]

    @swagger_auto_schema(
        tags=['Admin Account Project'],
        responses={200: AdminProjectImagesSerializer(many=False)}
    )
    def get(self, request, pk):
        instances = get_object_or_404(ProjectImage, id=pk)
        serializer = AdminProjectImagesSerializer(instances, context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        tags=['Admin Account Project'],
        request_body=AdminProjectImageSerializer
    )
    def put(self, request, pk):
        instance = get_object_or_404(ProjectImage, id=pk)
        # Make sure to check that data is not a list, but a dictionary
        serializer = AdminProjectImageSerializer(instance=instance, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        tags=['Admin Account Project'],
        responses={204:  'No Content'}
    )
    def delete(self, request, pk):
        project_delete = get_object_or_404(ProjectImage, id=pk)
        project_delete.delete()
        return Response({"message": "Изображение удален"}, status=status.HTTP_204_NO_CONTENT)
    

class ProjectFileView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]

    @swagger_auto_schema(
        tags=['Admin Account Project'],
        responses={200: AdminProjectFilesSerializer(many=False)}
    )
    def get(self, request, pk):
        instances = get_object_or_404(ProjectSmeta, id=pk)
        serializer = AdminProjectFilesSerializer(instances, context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        tags=['Admin Account Project'],
        request_body=AdminProjectFileSerializer
    )
    def put(self, request, pk):
        instance = get_object_or_404(ProjectSmeta, id=pk)
        # Make sure to check that data is not a list, but a dictionary
        serializer = AdminProjectFileSerializer(instance=instance, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        tags=['Admin Account Project'],
        responses={204:  'No Content'}
    )
    def delete(self, request, pk):
        project_delete = get_object_or_404(ProjectSmeta, id=pk)
        project_delete.delete()
        return Response({"message": "file удален"}, status=status.HTTP_204_NO_CONTENT)