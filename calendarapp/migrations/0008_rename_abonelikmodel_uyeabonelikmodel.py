# Generated by Django 3.2.3 on 2022-11-01 16:00

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('calendarapp', '0007_alter_etkinlikkatilimmodel_etkinlik'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AbonelikModel',
            new_name='UyeAbonelikModel',
        ),
    ]
