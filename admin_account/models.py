from django.db import models
from authen.models import CustomUser


class ProjectStatus(models.Model):
    name = models.CharField(max_length=250, verbose_name='Статус')

    def __str__(self):
        return self.name

    class Meta:
        db_table = "project_status"
        verbose_name = "Проекта статус"
        verbose_name_plural = "Проекта статус"


class Project(models.Model):
    address = models.CharField(max_length=250, verbose_name='Адрес')
    opening_date = models.DateField(verbose_name='Дата открытия')
    submission_deadline = models.DateField(verbose_name='Дедлайн по сдаче')
    contractor = models.ManyToManyField(CustomUser, blank=True, related_name='contractor', verbose_name='Подрядчики')
    status = models.ForeignKey(ProjectStatus, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Статус')
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='onwer', verbose_name='Создатель')
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address

    class Meta:
        db_table = "project"
        verbose_name = "Проекта"
        verbose_name_plural = "Проекта"


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Проекта', related_name='project_image')
    image = models.ImageField(upload_to='project_image/', null=True, blank=True, verbose_name='Изображение проекта')

    def __str__(self):
        return f'{self.project.address}'

    class Meta:
        db_table = "project_image"
        verbose_name = "Изображение проекта"
        verbose_name_plural = "Изображение проекта"


class ProjectSmeta(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Проекта', related_name='project_files')
    files = models.FileField(upload_to='project_files/', null=True, blank=True, verbose_name='Файл проекта')

    def __str__(self):
        return f'{self.project.address}'

    class Meta:
        db_table = "project_file"
        verbose_name = "Файл проекта"
        verbose_name_plural = "Файл проекта"
