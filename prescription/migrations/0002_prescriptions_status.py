# Generated by Django 5.1.2 on 2024-10-19 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prescription', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='prescriptions',
            name='status',
            field=models.IntegerField(choices=[(1, 'В обработке'), (3, 'Устранено'), (4, 'Просрочено'), (5, 'Null')], default=1, verbose_name='Статус'),
        ),
    ]