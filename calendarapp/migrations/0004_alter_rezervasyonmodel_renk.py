# Generated by Django 3.2.13 on 2022-06-08 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendarapp', '0003_auto_20220608_1528'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rezervasyonmodel',
            name='renk',
            field=models.CharField(choices=[('red', 'Kırmızı'), ('blue', 'Mavi')], default='gray', max_length=20, verbose_name='Renk'),
        ),
    ]