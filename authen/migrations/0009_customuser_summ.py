# Generated by Django 5.1.2 on 2024-11-08 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authen', '0008_alter_customuser_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='summ',
            field=models.FloatField(blank=True, null=True, verbose_name='Сумма штрафа'),
        ),
    ]