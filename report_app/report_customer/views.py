from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema

from utils.pagination import PaginationList
from utils.renderers import UserRenderers
from utils.permissions import IsCustomer

from report_app.models import ReportsName
from report_app.reports.serializers import ReportsNamesSerializer
from report_app.report_customer.serializers import ReportsNameCustomerSerializer


class CustomerReporNewView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsCustomer]
    pagination_class = PaginationList

    @swagger_auto_schema(
        tags=['Report Customer'],
        responses={200: ReportsNamesSerializer(many=True)},
        operation_summary='New report'
    )
    def get(self, request):
        instances = ReportsName.objects.filter(status_customer=1).order_by('-id')
        # Pagination logic
        paginator = self.pagination_class()
        paginated_instances = paginator.paginate_queryset(instances, request)
        serializer = ReportsNamesSerializer(paginated_instances, many=True, context={'request':request})
        return paginator.get_paginated_response(serializer.data)


class CustomerReporReceivedView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsCustomer]
    pagination_class = PaginationList

    @swagger_auto_schema(
        tags=['Report Customer'],
        responses={200: ReportsNamesSerializer(many=True)},
        operation_summary='Reports received'
    )
    def get(self, request):
        instances = ReportsName.objects.filter(customer=request.user, status_customer=3).order_by('-id')
        # Pagination logic
        paginator = self.pagination_class()
        paginated_instances = paginator.paginate_queryset(instances, request)
        serializer = ReportsNamesSerializer(paginated_instances, many=True, context={'request':request})
        return paginator.get_paginated_response(serializer.data)


class CustomerReportReturnView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsCustomer]
    pagination_class = PaginationList

    @swagger_auto_schema(
        tags=['Report Customer'],
        responses={200: ReportsNamesSerializer(many=True)},
        operation_summary='Returned reports'
    )
    def get(self, request):
        instances = ReportsName.objects.filter(customer=request.user, status_customer=4).order_by('-id')
        # Pagination logic
        paginator = self.pagination_class()
        paginated_instances = paginator.paginate_queryset(instances, request)
        serializer = ReportsNamesSerializer(paginated_instances, many=True, context={'request':request})
        return paginator.get_paginated_response(serializer.data)
    

class CustomerReportsView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsCustomer]
    pagination_class = PaginationList

    @swagger_auto_schema(
        tags=['Report Customer'],
        responses={200: ReportsNamesSerializer(many=True)},
        operation_summary='Submitted reports'
    )
    def get(self, request):
        instances = ReportsName.objects.filter(customer=request.user, status_customer=2).order_by('-id')
        # Pagination logic
        paginator = self.pagination_class()
        paginated_instances = paginator.paginate_queryset(instances, request)
        serializer = ReportsNamesSerializer(paginated_instances, many=True, context={'request':request})
        return paginator.get_paginated_response(serializer.data)
    
    @swagger_auto_schema(
        tags=['Report Customer'],
        request_body=ReportsNameCustomerSerializer,
        operation_summary='Submit a report.'
    )
    def post(self, request):
        serializer = ReportsNameCustomerSerializer(data=request.data, context={'customer':request.user, 'request':request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerReportView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsCustomer]

    @swagger_auto_schema(
        tags=['Report Customer'],
        responses={200: ReportsNamesSerializer(many=False)}
    )
    def get(self, request, pk):
        instances = get_object_or_404(ReportsName, id=pk)
        serializer = ReportsNamesSerializer(instances, context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        tags=['Report Customer'],
        request_body=ReportsNameCustomerSerializer,
    )
    def put(self, request, pk):
        instance = get_object_or_404(ReportsName, id=pk)
        # Make sure to check that data is not a list, but a dictionary
        serializer = ReportsNameCustomerSerializer(instance=instance, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        tags=['Report Customer'],
        responses={204:  'No Content'}
    )
    def delete(self, request, pk):
        report_delete = get_object_or_404(ReportsName, id=pk)
        report_delete.delete()
        return Response({"message": "Отчет удален"}, status=status.HTTP_204_NO_CONTENT)