# Generated by Django 3.2.13 on 2022-11-21 15:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('calendarapp', '0011_auto_20221104_1209'),
    ]

    operations = [
        migrations.AddField(
            model_name='rezervasyonmodel',
            name='misafir',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Misafir'),
        ),
        migrations.AlterField(
            model_name='rezervasyonmodel',
            name='onem_derecesi',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Önem Derecesi'),
        ),
        migrations.AlterField(
            model_name='rezervasyonmodel',
            name='uye',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rezervasyonlar', to='calendarapp.uyemodel', verbose_name='Üye'),
        ),
    ]
