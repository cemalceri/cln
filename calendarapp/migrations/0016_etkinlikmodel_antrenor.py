# Generated by Django 3.2.13 on 2022-07-24 13:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('calendarapp', '0015_antrenormodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='etkinlikmodel',
            name='antrenor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='anternor', to='calendarapp.antrenormodel', verbose_name='Antrenör'),
        ),
    ]
