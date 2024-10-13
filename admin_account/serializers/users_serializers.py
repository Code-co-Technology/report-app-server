from rest_framework import serializers
from django.contrib.auth.models import Group

from authen.models import CustomUser, Company


class UsersGroupSerizliers(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ['id', 'name']


class CompanySerializers(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = ['id', 'name_company', 'inn_company', 'ogrn', 'yurdik_address', 'logo']


class UsersSerializer(serializers.ModelSerializer):
    groups = UsersGroupSerizliers(many=True)
    company = CompanySerializers(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'phone', 'avatar', 'activate_profile', 'company', 'groups']


class ActivateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id', 'activate_profile']

    def update(self, instance, validated_data):
        instance.activate_profile = validated_data.get('activate_profile', instance.activate_profile)
        instance.save()

        return instance
