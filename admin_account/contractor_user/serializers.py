from rest_framework import serializers
from django.contrib.auth.models import Group

from authen.models import CustomUser, Company, Overdue, FailedReports
from report_app.models import ReportsName
from prescription.models import Prescriptions


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
    last_report_date = serializers.SerializerMethodField()
    last_project = serializers.SerializerMethodField()

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
            'block_sending_report',
            'last_report_date',
            'last_project',
        ]
    
    def get_last_report_date(self, obj):
        # Foydalanuvchiga tegishli oxirgi hisobotni topish
        last_report = ReportsName.objects.filter(constructor=obj).order_by('-create_at').first()
        if last_report:
            return last_report.create_at
        return None

    def get_last_project(self, obj):
        # Foydalanuvchiga tegishli oxirgi loyihani olish
        last_project = Prescriptions.objects.filter(contractor=obj).order_by('-create_at').first()
        if last_project:
            return last_project.project.address  # loyihaning nomini qaytarish
        return None


class AdminContractorUserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id', 'activate_profile', 'overdue', 'failed_reports', 'penalty', 'block_contractor', 'block_sending_report']
    
    def update(self, instance, validated_data):
        # Update user fields
        instance.activate_profile = validated_data.get('activate_profile', instance.activate_profile)
        instance.overdue = validated_data.get('overdue', instance.overdue)
        instance.failed_reports = validated_data.get('failed_reports', instance.failed_reports)
        instance.penalty = validated_data.get('penalty', instance.penalty)
        instance.block_contractor = validated_data.get('block_contractor', instance.block_contractor)
        instance.block_sending_report = validated_data.get('block_sending_report', instance.block_sending_report)

        instance.save()
        return instance
