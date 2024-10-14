from rest_framework import serializers
from django.contrib.auth.models import Group

from authen.models import CustomUser, Company, Overdue, FailedReports


class AdminUserGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ['id', 'name']


class AdminCompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = ['id', 'name_company', 'inn_company', 'ogrn', 'yurdik_address', 'logo']


class AdminOverdueSerializer(serializers.ModelSerializer):

    class Meta:
        model = Overdue
        fields = ['id', 'name']


class AdminFailedReportsSerializer(serializers.ModelSerializer):

    class Meta:
        model = FailedReports
        fields = ['id', 'name']


class AdminContractorUserSerializer(serializers.ModelSerializer):
    groups = AdminUserGroupSerializer(many=True)
    company = AdminCompanySerializer(read_only=True)
    overdue = AdminOverdueSerializer(read_only=True)
    failed_reports = AdminFailedReportsSerializer(read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'phone',
            'avatar',
            'activate_profile',
            'groups',
            'company',
            'overdue',
            'failed_reports',
            'penalty',
            'block_contractor',
            'block_sending_report'
        ]


class AdminContractorUserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id', 'overdue', 'failed_reports', 'penalty', 'block_contractor', 'block_sending_report']
    
    def update(self, instance, validated_data):
        # Update user fields
        instance.overdue = validated_data.get('overdue', instance.overdue)
        instance.failed_reports = validated_data.get('failed_reports', instance.failed_reports)
        instance.penalty = validated_data.get('penalty', instance.penalty)
        instance.block_contractor = validated_data.get('block_contractor', instance.block_contractor)
        instance.block_sending_report = validated_data.get('block_sending_report', instance.block_sending_report)

        instance.save()
        return instance
