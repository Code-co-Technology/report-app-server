from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema

from utils.pagination import PaginationList
from utils.renderers import UserRenderers
from utils.permissions import IsUser

from report_app.models import ReportsName
from report_app.reports.serializers import ReportsNamesSerializer
from report_app.report_user.serializers import ReportsNameCreateSerializer



class UserReportCount(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsUser]

    @swagger_auto_schema(
        tags=['Report User'],
        responses={200: ReportsNamesSerializer(many=True)},
    )
    def get(self, request):
        report_send = ReportsName.objects.filter(user=request.user.id, status_user=1).count()
        report_return = ReportsName.objects.filter(user=request.user.id, status_user=3).count()
        report_accepted = ReportsName.objects.filter(user=request.user.id, status_user=2).count()

        return Response({'report_send': report_send, 'report_return': report_return, 'report_accepted': report_accepted}, status=status.HTTP_200_OK)
    


class UserReportReceivedView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsUser]
    pagination_class = PaginationList

    @swagger_auto_schema(
        tags=['Report User'],
        responses={200: ReportsNamesSerializer(many=True)},
        operation_summary='Reports received'
    )
    def get(self, request):
        instances = ReportsName.objects.filter(user=request.user.id, status_user=2).order_by('-id')
        # Pagination logic
        paginator = self.pagination_class()
        paginated_instances = paginator.paginate_queryset(instances, request)
        serializer = ReportsNamesSerializer(paginated_instances, many=True, context={'request':request})
        return paginator.get_paginated_response(serializer.data)


class UserReportReturnView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsUser]
    pagination_class = PaginationList

    @swagger_auto_schema(
        tags=['Report User'],
        responses={200: ReportsNamesSerializer(many=True)},
        operation_summary='Returned reports'
    )
    def get(self, request):
        instances = ReportsName.objects.filter(user=request.user.id, status_user=3).order_by('-id')
        # Pagination logic
        paginator = self.pagination_class()
        paginated_instances = paginator.paginate_queryset(instances, request)
        serializer = ReportsNamesSerializer(paginated_instances, many=True, context={'request':request})
        return paginator.get_paginated_response(serializer.data)


class UserReportsView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsUser]
    parser_classes = (MultiPartParser, JSONParser)
    pagination_class = PaginationList

    @swagger_auto_schema(
        tags=['Report User'],
        responses={200: ReportsNamesSerializer(many=True)},
        operation_summary='Submitted reports'
    )
    def get(self, request, *args, **kwargs):
        instances = ReportsName.objects.filter(user=request.user.id, status_user=1).order_by('-id')
        # Pagination logic
        paginator = self.pagination_class()
        paginated_instances = paginator.paginate_queryset(instances, request)
        serializer = ReportsNamesSerializer(paginated_instances, many=True, context={'request':request})
        return paginator.get_paginated_response(serializer.data)
    
    @swagger_auto_schema(
        tags=['Report User'],
        request_body=ReportsNameCreateSerializer,
        operation_summary='Submit a report.'
    )
    def post(self, request):
        serializer = ReportsNameCreateSerializer(data=request.data, context={'user':request.user, 'request':request, 'company':request.user.compnay})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserReportView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsUser]

    @swagger_auto_schema(
        tags=['Report User'],
        responses={200: ReportsNamesSerializer(many=False)}
    )
    def get(self, request, pk):
        instances = get_object_or_404(ReportsName, user=request.user, id=pk)
        serializer = ReportsNamesSerializer(instances, context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        tags=['Report User'],
        request_body=ReportsNameCreateSerializer,
    )
    def put(self, request, pk):
        instance = get_object_or_404(ReportsName, user=request.user, id=pk)
        # Make sure to check that data is not a list, but a dictionary
        serializer = ReportsNameCreateSerializer(instance=instance, data=request.data, context={'user': request.user, 'request': request}, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        tags=['Report User'],
        responses={204:  'No Content'}
    )
    def delete(self, request, pk):
        report_delete = get_object_or_404(ReportsName, user=request.user, id=pk)
        report_delete.delete()
        return Response({"message": "Отчет удален"}, status=status.HTTP_204_NO_CONTENT)