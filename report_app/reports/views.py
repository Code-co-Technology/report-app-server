from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema

from utils.pagination import PaginationList
from utils.renderers import UserRenderers
from utils.permissions import IsLogin

from admin_account.models import Project
from report_app.models import Bob, TypeWork, ReportFile
from report_app.reports.serializers import BobSerializers, TypeOfWorkSerializer, RepostFileUpdateSerializer, RepostFileSerializer, ProjectReportSerializer


class ReportProjectView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsLogin]

    @swagger_auto_schema(
        tags=['Report'],
        responses={200: ProjectReportSerializer(many=True)},
        operation_summary='Section Reports'
    )
    def get(self, request):
        instances = Project.objects.filter(status__id=1).order_by('-id')
        serializer = ProjectReportSerializer(instances, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class BobView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsLogin]

    @swagger_auto_schema(
        tags=['Report'],
        responses={200: BobSerializers(many=True)},
        operation_summary='Section Reports'
    )
    def get(self, request):
        instances = Bob.objects.all().order_by('-id')
        serializer = BobSerializers(instances, many=True, context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class TypeOfWorkView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsLogin]

    @swagger_auto_schema(
        tags=['Report'],
        responses={200: TypeOfWorkSerializer(many=True)},
        operation_summary='Type of work Reports'
    )
    def get(self, request):
        instances = TypeWork.objects.all().order_by('-id')
        serializer = TypeOfWorkSerializer(instances, many=True, context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class RepostsFileDetaileView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsLogin]

    @swagger_auto_schema(
        tags=['Report'],
        responses={200: RepostFileSerializer(many=False)}
    )
    def get(self, request, pk):
        instances = get_object_or_404(ReportFile, id=pk)
        serializer = RepostFileSerializer(instances, context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        tags=['Report'],
        request_body=RepostFileUpdateSerializer
    )
    def put(self, request, pk):
        instance = get_object_or_404(ReportFile, id=pk)
        # Make sure to check that data is not a list, but a dictionary
        serializer = RepostFileUpdateSerializer(instance=instance, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        tags=['Report'],
        responses={204:  'No Content'}
    )
    def delete(self, request, pk):
        project_delete = get_object_or_404(ReportFile, id=pk)
        project_delete.delete()
        return Response({"message": "file удален"}, status=status.HTTP_204_NO_CONTENT)