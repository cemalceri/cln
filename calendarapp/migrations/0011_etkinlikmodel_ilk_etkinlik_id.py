# Generated by Django 3.2.13 on 2022-06-22 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendarapp', '0010_auto_20220614_1941'),
    ]

    operations = [
        migrations.AddField(
            model_name='etkinlikmodel',
            name='ilk_etkinlik_id',
            field=models.IntegerField(blank=True, null=True, verbose_name='İlk Etkinlik ID'),
        ),
    ]
