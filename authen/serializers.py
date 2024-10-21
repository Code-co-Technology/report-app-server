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

from authen.models import CustomUser, Company, Overdue, FailedReports
from report_app.models import ReportsName

class IncorrectCredentialsError(serializers.ValidationError):
    pass


class UnverifiedAccountError(serializers.ValidationError):
    pass


class UserGroupSerizliers(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']

class CompanySerializers(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = ['id', 'name_company', 'inn_company', 'ogrn', 'yurdik_address', 'logo']


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
    
    def validate(self, attrs):
        email = attrs.get('email')
        phone = attrs.get('phone')
        name_company = attrs.get('name_company')
        inn_company = attrs.get('inn_company')
        ogrn = attrs.get('ogrn')

        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error': 'Электронная почта должна быть уникальной. Этот адрес электронной почты принадлежит другому пользователю.'})

        if CustomUser.objects.filter(phone=phone).exists():
            raise serializers.ValidationError({'error': 'Номер телефона должен быть уникальным. Этот номер телефона принадлежит другому пользователю.'})

        if name_company and Company.objects.filter(name_company=name_company).exists():
            raise serializers.ValidationError({'error': 'Название компании должно быть уникальным.'})

        if inn_company and Company.objects.filter(inn_company=inn_company).exists():
            raise serializers.ValidationError({'error': 'ИНН должен быть уникальным.'})

        if ogrn and Company.objects.filter(ogrn=ogrn).exists():
            raise serializers.ValidationError({'error': 'ОГРН должен быть уникальным.'})

        return attrs

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

        groups_data = Group.objects.get(name='contractors')
        create.groups.add(groups_data)

        return create


class UserCustumerRegisterSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=50, validators=[
            MaxLengthValidator(limit_value=50, message='Имя не может превышать 50 символов.')],)
    last_name = serializers.CharField(max_length=50, validators=[
            MaxLengthValidator(limit_value=50, message='фамиля не может превышать 50 символов.')],)
    username = serializers.CharField(max_length=255, read_only=True) 
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(validators=[UniqueValidator(queryset=CustomUser.objects.all())])

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'phone', 'password', 'confirm_password']
        extra_kwargs = {'first_name': {'required': True}, 'last_name': {'required': True}}

    def validate_password(self, value):

        try:
            validate_password(value)
        except ValidationError as exc:
            raise serializers.ValidationError(str(exc))

        return value
    
    def validate(self, attrs):
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
        email = validated_data.get('email')
        username = email.split("@")[0]

        create = get_user_model().objects.create_user(username=username, **validated_data)

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
    company = CompanySerializers(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'phone', 'avatar', 'activate_profile', 'groups', 'company']


class UserInformationAdminSerializer(serializers.ModelSerializer):
    groups = UserGroupSerizliers(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'phone', 'avatar', 'groups']


class OverdueSerializer(serializers.ModelSerializer):

    class Meta:
        model = Overdue
        fields = ['id', 'name']


class FailedReportsSerializer(serializers.ModelSerializer):

    class Meta:
        model = FailedReports
        fields = ['id', 'name']

class UserInformationContractorSerializer(serializers.ModelSerializer):
    groups = UserGroupSerizliers(many=True, read_only=True)
    overdue = OverdueSerializer(read_only=True)
    failed_reports = FailedReportsSerializer(read_only=True)
    company = CompanySerializers(read_only=True)
    last_report_date = serializers.SerializerMethodField()

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
            'last_report_date'
        ]

    def get_last_report_date(self, obj):
        # Foydalanuvchiga tegishli oxirgi hisobotni topish
        last_report = ReportsName.objects.filter(constructor=obj).order_by('-create_at').first()
        if last_report:
            return last_report.create_at
        return None


class UserInformationCustomerSerializer(serializers.ModelSerializer):
    groups = UserGroupSerizliers(many=True, read_only=True)

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


class UserUpdateSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=True, max_length=30, validators=[UniqueValidator(queryset=CustomUser.objects.all()),
            MaxLengthValidator(limit_value=20, message="Длина адреса электронной почты не может превышать 30 символов.")],)
    avatar = serializers.ImageField(max_length=None, allow_empty_file=False, allow_null=False, use_url=False, required=False,)
    phone = serializers.CharField(required=True, max_length=15, validators=[UniqueValidator(queryset=CustomUser.objects.all()),
            MaxLengthValidator(limit_value=20, message="Длина Телефон не может превышать 15 символов.")],)
    name_company = serializers.CharField(max_length=250, required=False, allow_blank=True)
    inn_company = serializers.CharField(max_length=250, required=False, allow_blank=True)
    ogrn = serializers.CharField(max_length=250, required=False, allow_blank=True)
    yurdik_address = serializers.CharField(max_length=250, required=False, allow_blank=True)
    logo = serializers.ImageField(required=False, allow_null=True)
    

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'avatar', 'name_company', 'inn_company', 'ogrn', 'yurdik_address', 'logo']

    def validate(self, attrs):
        email = attrs.get('email')
        phone = attrs.get('phone')
        name_company = attrs.get('name_company')
        inn_company = attrs.get('inn_company')
        ogrn = attrs.get('ogrn')

        # Check for unique email and phone
        if email and CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': 'Электронная почта должна быть уникальной.'})
        
        if phone and CustomUser.objects.filter(phone=phone).exists():
            raise serializers.ValidationError({'phone': 'Телефон должен быть уникальным.'})
        
        # Check for unique company fields
        if name_company and Company.objects.filter(name_company=name_company).exists():
            raise serializers.ValidationError({'name_company': 'Название компании должно быть уникальным.'})

        if inn_company and Company.objects.filter(inn_company=inn_company).exists():
            raise serializers.ValidationError({'inn_company': 'ИНН компании должен быть уникальным.'})

        if ogrn and Company.objects.filter(ogrn=ogrn).exists():
            raise serializers.ValidationError({'ogrn': 'ОГРН компании должен быть уникальным.'})

        return attrs

    def update(self, instance, validated_data):
        # Update user fields
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)

        if instance.avatar == None:
            instance.avatar = self.context.get("avatar")
        else:
            instance.avatar = validated_data.get("avatar", instance.avatar)

        # Update or create company if necessary
        if any([validated_data.get('name_company'), validated_data.get('inn_company'), validated_data.get('ogrn')]):
            company_data = {
                'name_company': validated_data.get('name_company'),
                'inn_company': validated_data.get('inn_company'),
                'ogrn': validated_data.get('ogrn'),
                'yurdik_address': validated_data.get('yurdik_address'),
                'logo': validated_data.get('logo')
            }
            if instance.company:
                # Update existing company
                for key, value in company_data.items():
                    if value is not None:
                        setattr(instance.company, key, value)
                instance.company.save()
            else:
                # Create new company
                instance.company = Company.objects.create(**company_data)

        instance.save()
        return instance


class ChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate(self, data):
        """
        Проверьте, совпадает ли new_password с confirmed_password.
        """
        if data.get("new_password") != data.get("confirm_password"):
            raise serializers.ValidationError("Новый пароль и подтверждение пароля должны совпадать.")

        return data


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        fields = ["email"]


class PasswordResetCompleteSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=8, max_length=32, write_only=True)
    confirm_password = serializers.CharField(min_length=8, max_length=32, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields = ["password", "confirm_password", "token", "uidb64"]

    def validate(self, attrs):
        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")
        token = attrs.get("token")
        uidb64 = attrs.get("uidb64")

        if password != confirm_password:
            raise serializers.ValidationError({"error": "Пароли не совпадают"})

        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed("Неверная ссылка", 401)

            user.set_password(password)
            user.save()
            return user
        except Exception:
            raise AuthenticationFailed("Неверная ссылка", 401)