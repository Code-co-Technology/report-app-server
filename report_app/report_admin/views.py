from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema

from utils.pagination import PaginationList
from utils.renderers import UserRenderers
from utils.permissions import IsAdmin

from report_app.models import ReportsName
from report_app.reports.serializers import ReportsNamesSerializer
from report_app.report_admin.serializers import ReportsNameAdminSerializer
    

class AdminReportsView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]
    pagination_class = PaginationList

    @swagger_auto_schema(
        tags=['Report Admin'],
        responses={200: ReportsNamesSerializer(many=True)},
        operation_summary='Reports'
    )
    def get(self, request):
        instances = ReportsName.objects.filter(constructor=request.user, status_contractor=2).order_by('-id')
        # Pagination logic
        paginator = self.pagination_class()
        paginated_instances = paginator.paginate_queryset(instances, request)
        serializer = ReportsNamesSerializer(paginated_instances, many=True, context={'request':request})
        return paginator.get_paginated_response(serializer.data)


class AdminReportView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]

    @swagger_auto_schema(
        tags=['Report Admin'],
        responses={200: ReportsNamesSerializer(many=False)}
    )
    def get(self, request, pk):
        instances = get_object_or_404(ReportsName, id=pk)
        serializer = ReportsNamesSerializer(instances, context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        tags=['Report Admin'],
        request_body=ReportsNameAdminSerializer,
    )
    def put(self, request, pk):
        instance = get_object_or_404(ReportsName, id=pk)
        # Make sure to check that data is not a list, but a dictionary
        serializer = ReportsNameAdminSerializer(instance=instance, data=request.data, context={'admin':request.user, 'request': request}, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        tags=['Report Admin'],
        responses={204:  'No Content'}
    )
    def delete(self, request, pk):
        report_delete = get_object_or_404(ReportsName, constructor=request.user, id=pk)
        report_delete.delete()
        return Response({"message": "Отчет удален"}, status=status.HTTP_204_NO_CONTENT)
