# Generated by Django 5.1.2 on 2024-10-14 10:48

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_account', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='contractor',
        ),
        migrations.AddField(
            model_name='project',
            name='contractor',
            field=models.ManyToManyField(blank=True, related_name='contractor', to=settings.AUTH_USER_MODEL, verbose_name='Подрядчики'),
        ),
    ]