# Generated by Django 5.1.2 on 2024-10-21 17:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_account', '0004_alter_projectsmeta_files'),
        ('prescription', '0004_remove_prescriptions_contractor_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prescriptions',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_prescription', to='admin_account.project', verbose_name='Проект'),
        ),
    ]
