# Generated by Django 3.2.13 on 2022-06-14 16:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('calendarapp', '0007_auto_20220610_1119'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='etkinlikmodel',
            options={'ordering': ['-id'], 'verbose_name': 'Etkinlik', 'verbose_name_plural': 'Etkinlikler'},
        ),
        migrations.CreateModel(
            name='MusteriModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('adi', models.CharField(max_length=250, verbose_name='Adı')),
                ('soyadi', models.CharField(max_length=250, verbose_name='Soyadı')),
                ('kimlikNo', models.CharField(blank=True, max_length=11, null=True, verbose_name='KimlikNo')),
                ('telefon', models.CharField(blank=True, max_length=11, null=True, verbose_name='Telefon')),
                ('email', models.EmailField(blank=True, max_length=250, null=True, verbose_name='E-Mail')),
                ('adres', models.TextField(blank=True, max_length=250, null=True, verbose_name='Adres')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='uye', to=settings.AUTH_USER_MODEL, verbose_name='Ekleyen')),
            ],
            options={
                'verbose_name': 'Müşteri',
                'verbose_name_plural': 'Müşteriler',
                'ordering': ['-id'],
            },
        ),
        migrations.AddField(
            model_name='etkinlikmodel',
            name='uye',
            field=models.ManyToManyField(blank=True, to='calendarapp.MusteriModel', verbose_name='Üye'),
        ),
    ]
