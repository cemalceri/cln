# Generated by Django 3.2.13 on 2022-07-24 13:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('calendarapp', '0014_alter_kortmodel_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='AntrenorModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('adi', models.CharField(max_length=250, verbose_name='Adı')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='antrenor', to=settings.AUTH_USER_MODEL, verbose_name='Ekleyen')),
            ],
            options={
                'verbose_name': 'Antrenor',
                'verbose_name_plural': 'Antrenor',
                'ordering': ['id'],
            },
        ),
    ]
