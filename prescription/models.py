from django.db import models

from authen.models import CustomUser
from admin_account.models import Project


class TypeOfViolation(models.Model):
    name = models.CharField(max_length=250, verbose_name='Тип нарушения')

    def __str__(self):
        return self.name

    class Meta:
        db_table = "type_of_violation"
        verbose_name = "Тип нарушения"
        verbose_name_plural = "Тип нарушения"


class Prescriptions(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='Проект')
    contractor = models.ManyToManyField(CustomUser, verbose_name='Подрядчик')
    type_violation = models.ManyToManyField(TypeOfViolation, blank=True, verbose_name='Тип нарушения')
    deadline = models.DateField(verbose_name='Срок устранения')
    STATUS = (
        (1, 'В обработке'),
        (3, 'Устранено'),
        (4, 'Просрочено'),
        (5, 'Null'),
    )
    status = models.IntegerField(choices=STATUS, default=1, verbose_name='Статус')
    owner = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='owner', verbose_name='Владелец')
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.project.address}'

    class Meta:
        db_table = "prescriptions"
        verbose_name = "Предписания"
        verbose_name_plural = "Предписания"


class PrescriptionsImage(models.Model):
    prescription = models.ForeignKey(Prescriptions, on_delete=models.CASCADE, null=True, blank=True, related_name='prescription_image')
    image = models.ImageField(upload_to='prescriptions_image', verbose_name='Предписания изображение')

    class Meta:
        db_table = "prescriptions_image"
        verbose_name = "Предписания изображение"
        verbose_name_plural = "Предписания изображение"


class PrescriptionsComment(models.Model):
    prescription = models.ForeignKey(Prescriptions, on_delete=models.CASCADE, null=True, blank=True, related_name='prescription_comment')
    comment = models.TextField(null=True, blank=True, verbose_name='Предписания комментарий')
    owner = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Владелец')
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "prescriptions_comment"
        verbose_name = "Предписания комментарий"
        verbose_name_plural = "Предписания комментарий"