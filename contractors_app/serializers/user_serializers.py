from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator

from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from authen.models import CustomUser, Company


class ContractorGorupsUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ['id', 'name']


class IncorrectCredentialsError(serializers.ValidationError):
    pass

class UnverifiedAccountError(serializers.ValidationError):
    pass

class ContractorAddUserSerializer(serializers.ModelSerializer):
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
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'phone', 'password', 'confirm_password', 'company', 'groups']
        extra_kwargs = {'first_name': {'required': True}, 'last_name': {'required': True}}

    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as exc:
            raise serializers.ValidationError(str(exc))
        return value
    
    def validate(self, attrs):
        # Check for unique email and phone
        email = attrs.get('email')
        phone = attrs.get('phone')

        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error': 'Электронная почта должна быть уникальной. Этот адрес электронной почты принадлежит другому пользователю.'})

        if CustomUser.objects.filter(phone=phone).exists():
            raise serializers.ValidationError({'error': 'Номер телефона должен быть уникальным. Этот номер телефона принадлежит другому пользователю.'})

        return attrs

    def create(self, validated_data):
        if validated_data['password'] != validated_data['confirm_password']:
            raise serializers.ValidationError({'error': 'Эти пароли не совпадают.'})

        validated_data.pop('confirm_password')
        groups_data = validated_data.pop('groups', [])
        email = validated_data.get('email')

        username = email.split("@")[0]
        create = get_user_model().objects.create_user(username=username, **validated_data)
        create.activate_profile = True
        create.company = self.context.get('company')
        create.groups.set(groups_data)
        create.save()
        return create


class ContractorCompanySerializers(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = ['id', 'name_company', 'inn_company', 'ogrn', 'yurdik_address', 'logo']


class ContractorUsersSerializer(serializers.ModelSerializer):
    groups = ContractorGorupsUserSerializer(many=True)
    company = ContractorCompanySerializers(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'phone', 'avatar', 'activate_profile', 'company', 'groups']


class ContractorUserSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=True, max_length=30, validators=[UniqueValidator(queryset=CustomUser.objects.all()),
            MaxLengthValidator(limit_value=20, message='Длина адреса электронной почты не может превышать 30 символов.')],)
    avatar = serializers.ImageField(max_length=None, allow_empty_file=False, allow_null=False, use_url=False, required=False,)
    phone = serializers.CharField(required=True, max_length=15, validators=[UniqueValidator(queryset=CustomUser.objects.all()),
            MaxLengthValidator(limit_value=20, message='Длина Телефон не может превышать 15 символов.')],)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'phone', 'avatar', 'activate_profile', 'company', 'groups']
    
    def update(self, instance, validated_data):
        instance.email = validated_data.get("email", instance.email)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.phone = validated_data.get("phone", instance.phone)
        instance.activate_profile = validated_data.get("activate_profile", instance.activate_profile)

        # Update avatar only if provided
        if instance.avatar == None:
            instance.avatar = self.context.get("avatar")
        else:
            instance.avatar = validated_data.get("avatar", instance.avatar)

        # Update groups
        if 'groups' in validated_data:
            instance.groups.set(validated_data['groups'])

        instance.save()
        return instance