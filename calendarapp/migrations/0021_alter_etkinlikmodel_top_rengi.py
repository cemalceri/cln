# Generated by Django 3.2.13 on 2022-12-07 01:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendarapp', '0020_auto_20221203_2217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='etkinlikmodel',
            name='top_rengi',
            field=models.CharField(choices=[('red', 'Kırmızı'), ('blue', 'Mavi'), ('yellow', 'Sarı'), ('green', 'Yeşil')], default='gray', max_length=20, verbose_name='Top Rengi'),
        ),
    ]