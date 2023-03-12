# Generated by Django 4.1.7 on 2023-03-12 15:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('calendarapp', '0054_auto_20230306_0037'),
    ]

    operations = [
        migrations.AddField(
            model_name='antrenormodel',
            name='ucret_katsayisi',
            field=models.DecimalField(decimal_places=2, default=1.0, max_digits=4, verbose_name='Ücret Katsayısı'),
        ),
        migrations.AddField(
            model_name='parahareketimodel',
            name='etkinlik',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='etkinlik_parahareketi_relations', to='calendarapp.etkinlikmodel'),
        ),
    ]
