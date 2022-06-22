# Generated by Django 3.2.13 on 2022-06-14 19:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('calendarapp', '0009_auto_20220614_1938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uyegrupmodel',
            name='uye1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='uye1', to='calendarapp.uyemodel'),
        ),
        migrations.AlterField(
            model_name='uyegrupmodel',
            name='uye2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='uye2', to='calendarapp.uyemodel'),
        ),
        migrations.AlterField(
            model_name='uyegrupmodel',
            name='uye3',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='uye3', to='calendarapp.uyemodel'),
        ),
        migrations.AlterField(
            model_name='uyegrupmodel',
            name='uye4',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='uye4', to='calendarapp.uyemodel'),
        ),
        migrations.DeleteModel(
            name='EtkinlikMember',
        ),
    ]