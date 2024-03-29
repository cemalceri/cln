# Generated by Django 4.1.7 on 2023-03-22 01:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendarapp', '0056_alter_telafidersmodel_options_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='etkinlikmodel',
            old_name='top_rengi',
            new_name='seviye',
        ),
        migrations.RenameField(
            model_name='haftalikplanmodel',
            old_name='top_rengi',
            new_name='seviye',
        ),
        migrations.AddField(
            model_name='rezervasyonmodel',
            name='seviye',
            field=models.CharField(choices=[('Kirmizi', 'Kırmızı'), ('Turuncu', 'Turuncu'), ('Sari', 'Sarı'), ('Yesil', 'Yeşil'), ('Yetiskin', 'Yetişkin'), ('TenisOkulu', 'Tenis Okulu')], default='red', max_length=20, verbose_name='Seviye'),
        ),
        migrations.AddField(
            model_name='uyemodel',
            name='indirim_orani',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='İndirim Oranı'),
        ),
        migrations.AlterField(
            model_name='uyemodel',
            name='adres',
            field=models.CharField(default='Girilecek', max_length=250, verbose_name='Adres'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='uyemodel',
            name='cinsiyet',
            field=models.CharField(choices=[('Erkek', 'Erkek'), ('Kadın', 'Kadın')], default='Girilecek', max_length=10, verbose_name='Cinsiyet'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='uyemodel',
            name='referansi',
            field=models.CharField(default='Girilecek', max_length=50, verbose_name='Referans'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='uyemodel',
            name='seviye_rengi',
            field=models.CharField(choices=[('Kirmizi', 'Kırmızı'), ('Turuncu', 'Turuncu'), ('Sari', 'Sarı'), ('Yesil', 'Yeşil'), ('Yetiskin', 'Yetişkin'), ('TenisOkulu', 'Tenis Okulu')], default='red', max_length=20, verbose_name='Seviye'),
        ),
        migrations.AlterField(
            model_name='uyemodel',
            name='telefon',
            field=models.CharField(default='Girilecek', max_length=11, verbose_name='Telefon'),
            preserve_default=False,
        ),
    ]
