from rest_framework import serializers

from authen.serializers import UserInformationSerializer, UserInformationAdminSerializer, UserInformationContractorSerializer, UserInformationCustomerSerializer
from report_app.models import Bob, TypeWork, ReportsName, Reports, RespostComment


class BobSerializers(serializers.ModelSerializer):
    
     class Meta:
          model = Bob
          fields = ['id', 'name']


class TypeOfWorkSerializer(serializers.ModelSerializer):
     
     class Meta:
          model = TypeWork
          fields = ['id', 'name']


class ResportsCommentSerializer(serializers.ModelSerializer):

     class Meta:
          model = RespostComment
          fields = ['id', 'comment', 'owner', 'create_at']


class ResportsSerializer(serializers.ModelSerializer):
     bob = BobSerializers(read_only=True)
     type_work = TypeOfWorkSerializer(read_only=True)

     class Meta:
          model = Reports
          fields = [
               'id', 
               'bob', 
               'type_work', 
               'position',
               'quantity',
               'frame',
               'floor',
               'mark',
               'axles',
               'premises',
               'completions',
               'files',
               'create_at'
          ]


class ReportsNamesSerializer(serializers.ModelSerializer):
     respost_comment = ResportsCommentSerializer(many=True)
     user = UserInformationSerializer(read_only=True)
     constructor = UserInformationContractorSerializer(read_only=True)
     customer = UserInformationCustomerSerializer(read_only=True)
     admin =  UserInformationAdminSerializer(read_only=True)

     class Meta:
          model = ReportsName
          fields = [
               'id', 
               'name', 
               'respost_comment', 
               'constructor_accepted',
               'accepted_customer',
               'expired_customer',
               'expired_admin',
               'status',
               'user',
               'constructor',
               'customer',
               'admin',
               'create_at'
          ]
