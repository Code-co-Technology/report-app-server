from rest_framework import serializers

from authen.serializers import UserInformationSerializer, UserInformationAdminSerializer, UserInformationContractorSerializer, UserInformationCustomerSerializer
from report_app.models import Bob, TypeWork, ReportsName, Reports, RespostComment, ReportFile


class BobSerializers(serializers.ModelSerializer):
    
     class Meta:
          model = Bob
          fields = ['id', 'name']


class TypeOfWorkSerializer(serializers.ModelSerializer):
     
     class Meta:
          model = TypeWork
          fields = ['id', 'name']

class RepostFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReportFile
        fields = ['id', 'report_file', 'file']


class RepostFileUpdateSerializer(serializers.ModelSerializer):
     file = serializers.FileField(max_length=None, allow_empty_file=False, allow_null=False, use_url=False, required=False,)

     class Meta:
        model = ReportFile
        fields = ['id', 'report_file', 'file']
     
     def update(self, instance, validated_data):
        instance.file = validated_data.get('file', instance.files)

        if instance.file == None:
            instance.file = self.context.get("file")
        else:
            instance.file = validated_data.get("file", instance.files)

        instance.save()
        return instance


class ResportsCommentSerializer(serializers.ModelSerializer):

     class Meta:
          model = RespostComment
          fields = ['id', 'comment', 'owner', 'create_at']


class ResportsSerializer(serializers.ModelSerializer):
     bob = BobSerializers(read_only=True)
     type_work = TypeOfWorkSerializer(read_only=True)
     report_file = RepostFileSerializer(many=True)

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
               'report_file',
               'create_at'
          ]


class ReportsNamesSerializer(serializers.ModelSerializer):
     respost_comment = ResportsCommentSerializer(many=True)
     resposts = ResportsSerializer(many=True)
     user = UserInformationSerializer(read_only=True)
     constructor = UserInformationContractorSerializer(read_only=True)
     customer = UserInformationCustomerSerializer(read_only=True)
     admin =  UserInformationAdminSerializer(read_only=True)
     status_user = serializers.CharField(source='get_status_user_display')
     status_contractor = serializers.CharField(source='get_status_contractor_display')
     status_customer = serializers.CharField(source='get_status_customer_display')
     status = serializers.CharField(source='get_status_display')

     class Meta:
          model = ReportsName
          fields = [
               'id', 
               'name', 
               'user',
               'constructor',
               'customer',
               'respost_comment',
               'resposts',
               'status_user',
               'status_contractor',
               'status_customer',
               'status',
               'user',
               'constructor',
               'customer',
               'admin',
               'create_at'
          ]

