from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator

from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from authen.models import CustomUser, Company


class CustomerGorupsUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ['id', 'name']


class IncorrectCredentialsError(serializers.ValidationError):
    pass

class UnverifiedAccountError(serializers.ValidationError):
    pass

class CustumerAddUserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=50, validators=[
            MaxLengthValidator(limit_value=50, message='Имя не может превышать 50 символов.')],)
    last_name = serializers.CharField(max_length=50, validators=[
            MaxLengthValidator(limit_value=50, message='фамиля не может превышать 50 символов.')],)
    username = serializers.CharField(max_length=255, read_only=True) 
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(validators=[UniqueValidator(queryset=CustomUser.objects.all())])
    groups = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), many=True, required=False)


    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'phone', 'password', 'confirm_password', 'groups']
        extra_kwargs = {'first_name': {'required': True}, 'last_name': {'required': True}}

    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as exc:
            raise serializers.ValidationError(str(exc))
        return value

    def create(self, validated_data):
        if validated_data['password'] != validated_data['confirm_password']:
            raise serializers.ValidationError({'error': 'Эти пароли не совпадают.'})

        validated_data.pop('confirm_password')
        groups_data = validated_data.pop('groups', [])
        email = validated_data.get('email')

        username = email.split("@")[0]
        create = get_user_model().objects.create_user(username=username, **validated_data)
        create.groups.set(groups_data)
        return create


class CustomCompanySerializers(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = ['id', 'name_company', 'inn_company', 'ogrn', 'yurdik_address', 'logo']


class CustomUsersSerializer(serializers.ModelSerializer):
    groups = CustomerGorupsUserSerializer(many=True)
    company = CustomCompanySerializers(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'phone', 'avatar', 'activate_profile', 'company', 'groups']