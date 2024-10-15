from rest_framework import serializers
from django.contrib.auth.models import Group

from authen.models import CustomUser, Company
from admin_account.contractor_user.serializers import AdminUserGroupSerializer


class AdminCustumerUserSerializer(serializers.ModelSerializer):
    groups = AdminUserGroupSerializer(many=True)

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
            'activate_profile',
            'report_processing',
            'creating_prescriptions',
            'processing_orders',
        ]


class AdminCustumerUserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id', 'activate_profile', 'report_processing', 'creating_prescriptions', 'processing_orders']
    
    def update(self, instance, validated_data):
        # Update user fields
        instance.activate_profile = validated_data.get('activate_profile', instance.activate_profile)
        instance.report_processing = validated_data.get('report_processing', instance.report_processing)
        instance.creating_prescriptions = validated_data.get('creating_prescriptions', instance.creating_prescriptions)
        instance.processing_orders = validated_data.get('processing_orders', instance.processing_orders)

        instance.save()
        return instance
