from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone


class Overdue(models.Model):
    name = models.CharField(max_length=250, verbose_name='Просрочка')

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "overdue"
        verbose_name = "Просрочка"
        verbose_name_plural = "Просрочка"


class FailedReports(models.Model):
    name = models.CharField(max_length=250, verbose_name='Сроки')

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "failed_reports"
        verbose_name = "Проваленные отчеты"
        verbose_name_plural = "Проваленные отчеты"


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, username, password, **extra_fields)



class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name="E-mail")
    username = models.CharField(max_length=30, null=True, blank=True, unique=True, verbose_name="Логин")
    first_name = models.CharField(max_length=255, null=True, blank=True, verbose_name="Имя")
    last_name = models.CharField(max_length=255, null=True, blank=True, verbose_name="Фамилия")
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+9989999999'. Up to 15 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=250, null=True, blank=True, verbose_name="Телефон", unique=True)
    avatar = models.ImageField(upload_to="avatar/", null=True, blank=True, verbose_name="Изображение")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    activate_profile = models.BooleanField(default=False, verbose_name="Активировать профиль")
    overdue = models.ForeignKey(Overdue, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Просрочка. Для подрядчика')
    failed_reports = models.ForeignKey(FailedReports, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Проваленные отчеты. Для подрядчика')
    penalty = models.BooleanField(default=False, verbose_name='Штраф. Для подрядчика')
    block_contractor = models.BooleanField(default=False, verbose_name='Заблокировать подрядчика. Для подрядчика')
    block_sending_report = models.BooleanField(default=False, verbose_name='Заблокировать отправку  отчето. Для подрядчика')
    report_processing = models.BooleanField(default=False, verbose_name='Обработка отчетов. Для Сотрудники')
    creating_prescriptions = models.BooleanField(default=False, verbose_name='Создание предписаний. Для Сотрудники')
    processing_orders = models.BooleanField(default=False, verbose_name='Обработка предписаний. Для Сотрудники')
    company = models.ForeignKey(
        'Company', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name="Компания",
        related_name='company'

    )
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

    class Meta:
        db_table = "table_user"
        verbose_name = "Пользователи"
        verbose_name_plural = "Пользователи"


class Company(models.Model):
    name_company = models.CharField(max_length=250, null=True, blank=True, unique=True, verbose_name="Название компании")
    inn_company = models.CharField(max_length=250, null=True, blank=True, unique=True, verbose_name="ИНН")
    ogrn  = models.CharField(max_length=250, null=True, blank=True, unique=True, verbose_name="ОГРН")
    yurdik_address = models.CharField(max_length=250, null=True, blank=True, verbose_name='Юридический адрес')
    logo = models.ImageField(upload_to='logo/', null=True, blank=True, verbose_name='Логотип')

    def __str__(self):
        return self.name_company

    class Meta:
        db_table = "company"
        verbose_name = "Компании"
        verbose_name_plural = "Компании"