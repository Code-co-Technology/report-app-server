# Generated by Django 5.1.2 on 2024-10-24 14:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prescription', '0007_alter_prescriptioncontractor_unique_together_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='prescriptioncontractor',
            options={'verbose_name': 'Предписания Подрядчики', 'verbose_name_plural': 'Предписания Подрядчики'},
        ),
        migrations.AddField(
            model_name='prescriptioncontractor',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employee_for_prescription', to=settings.AUTH_USER_MODEL, verbose_name='Сотрудник'),
        ),
        migrations.AlterField(
            model_name='prescriptioncontractor',
            name='contractor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contractor_for_prescription', to=settings.AUTH_USER_MODEL, verbose_name='Подрядчик'),
        ),
        migrations.AlterField(
            model_name='prescriptioncontractor',
            name='prescription',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contractor_statuses', to='prescription.prescriptions', verbose_name='Предписания'),
        ),
        migrations.AlterUniqueTogether(
            name='prescriptioncontractor',
            unique_together={('prescription', 'contractor', 'user')},
        ),
        migrations.AlterModelTable(
            name='prescriptioncontractor',
            table='prescriptions_contratctor',
        ),
    ]