from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema

from utils.pagination import PaginationList
from utils.renderers import UserRenderers
from utils.permissions import IsLogin

from report_app.models import Bob, TypeWork
from report_app.reports.serializers import BobSerializers, TypeOfWorkSerializer


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