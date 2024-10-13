import email
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator

from django.contrib.auth.models import Group
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.exceptions import AuthenticationFailed

from authen.models import CustomUser, Company


class IncorrectCredentialsError(serializers.ValidationError):
    pass


class UnverifiedAccountError(serializers.ValidationError):
    pass


class UserGroupSerizliers(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']


class UserSignUpSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=50, validators=[
            MaxLengthValidator(limit_value=50, message='Имя не может превышать 50 символов.')],)
    last_name = serializers.CharField(max_length=50, validators=[
            MaxLengthValidator(limit_value=50, message='фамиля не может превышать 50 символов.')],)
    username = serializers.CharField(max_length=255, read_only=True) 
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(validators=[UniqueValidator(queryset=CustomUser.objects.all())])
    # Company fields for user registration
    name_company = serializers.CharField(max_length=250, required=False, allow_blank=True)
    inn_company = serializers.CharField(max_length=250, required=False, allow_blank=True)
    ogrn = serializers.CharField(max_length=250, required=False, allow_blank=True)
    yurdik_address = serializers.CharField(max_length=250, required=False, allow_blank=True)
    logo = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'phone', 'password', 'confirm_password', 'name_company', 'inn_company', 'ogrn', 'yurdik_address', 'logo']
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
        email = validated_data.get('email')
        username = email.split("@")[0]

        # Handle company creation if provided
        company_data = {
            'name_company': validated_data.pop('name_company', None),
            'inn_company': validated_data.pop('inn_company', None),
            'ogrn': validated_data.pop('ogrn', None),
            'yurdik_address': validated_data.pop('yurdik_address', None),
            'logo': validated_data.pop('logo', None)  # Handle logo field
        }

        company = None
        if any(company_data.values()):
            company = Company.objects.create(**company_data)

        
        create = get_user_model().objects.create_user(username=username, company=company, **validated_data)

        groups_data = Group.objects.get(name='customer')
        create.groups.add(groups_data)

        return create


class UserSigInSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=50, min_length=2)
    password = serializers.CharField(max_length=50, min_length=1)

    class Meta:
        model = get_user_model()
        fields = ['email', 'password']
        read_only_fields = ("email",)

    def validate(self, data):
        if self.context.get('request') and self.context['request'].method == 'POST':
            allowed_keys = set(self.fields.keys())
            input_keys = set(data.keys())
            extra_keys = input_keys - allowed_keys

            if extra_keys:
                raise serializers.ValidationError(f"Дополнительные ключи не допускаются: {', '.join(extra_keys)}")

        return data


class UserInformationSerializer(serializers.ModelSerializer):
    groups = UserGroupSerizliers(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'phone', 'avatar', 'activate_profile', 'groups']