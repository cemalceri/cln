# Generated by Django 3.2.13 on 2022-07-27 11:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('calendarapp', '0001_initial'),
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
        migrations.CreateModel(
            name='EtkinlikModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('baslik', models.CharField(max_length=200, verbose_name='Başlık')),
                ('baslangic_tarih_saat', models.DateTimeField(verbose_name='Başlangıç Tarih Saat')),
                ('bitis_tarih_saat', models.DateTimeField(verbose_name='Bitiş Tarih Saat')),
                ('renk', models.CharField(choices=[('red', 'Kırmızı'), ('blue', 'Mavi'), ('yellow', 'Sarı'), ('green', 'Yeşil')], default='gray', max_length=20, verbose_name='Renk')),
                ('tekrar', models.IntegerField(blank=True, null=True, verbose_name='Tekrar Sayısı')),
                ('aciklama', models.CharField(blank=True, max_length=500, null=True, verbose_name='Açıklama')),
                ('ilk_etkinlik_id', models.IntegerField(blank=True, null=True, verbose_name='İlk Etkinlik ID')),
                ('antrenor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='anternor', to='calendarapp.antrenormodel', verbose_name='Antrenör')),
            ],
            options={
                'verbose_name': 'Etkinlik',
                'verbose_name_plural': 'Etkinlikler',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='GunlerModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adi', models.CharField(max_length=250)),
                ('haftanin_gunu', models.IntegerField(verbose_name='Haftanın Kaçıncı Günü')),
                ('hafta_ici_mi', models.BooleanField(default=False, verbose_name='Hafta için mi')),
            ],
            options={
                'verbose_name': 'Günler',
                'verbose_name_plural': 'Günler',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='KortModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('adi', models.CharField(max_length=250, verbose_name='Adı')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='kort', to=settings.AUTH_USER_MODEL, verbose_name='Ekleyen')),
            ],
            options={
                'verbose_name': 'Kort',
                'verbose_name_plural': 'Kort',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='SaatlerModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adi', models.CharField(max_length=250)),
                ('baslangic_degeri', models.TimeField()),
                ('bitis_degeri', models.TimeField()),
            ],
            options={
                'verbose_name': 'Saatler',
                'verbose_name_plural': 'Saatler',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='UyeGrupModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Üye Grubu',
                'verbose_name_plural': 'Gruplar',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='UyeModel',
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
        migrations.AlterModelOptions(
            name='rezervasyonmodel',
            options={'ordering': ['id'], 'verbose_name': 'Rezervasyon', 'verbose_name_plural': 'Rezervasyon'},
        ),
        migrations.RemoveField(
            model_name='rezervasyonmodel',
            name='baslangic_tarih_saat',
        ),
        migrations.RemoveField(
            model_name='rezervasyonmodel',
            name='baslik',
        ),
        migrations.RemoveField(
            model_name='rezervasyonmodel',
            name='bitis_tarih_saat',
        ),
        migrations.AddField(
            model_name='rezervasyonmodel',
            name='adi',
            field=models.CharField(default='deneme', max_length=250, verbose_name='Adı'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rezervasyonmodel',
            name='onem_derecesi',
            field=models.IntegerField(default=0, verbose_name='Önem Derecesi'),
        ),
        migrations.AlterField(
            model_name='rezervasyonmodel',
            name='aciklama',
            field=models.TextField(blank=True, null=True, verbose_name='Açıklama'),
        ),
        migrations.AlterField(
            model_name='rezervasyonmodel',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rezervasyon', to=settings.AUTH_USER_MODEL, verbose_name='Ekleyen'),
        ),
        migrations.DeleteModel(
            name='RezervasyonMember',
        ),
        migrations.AddField(
            model_name='uyegrupmodel',
            name='uye1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='uye1', to='calendarapp.uyemodel'),
        ),
        migrations.AddField(
            model_name='uyegrupmodel',
            name='uye2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='uye2', to='calendarapp.uyemodel'),
        ),
        migrations.AddField(
            model_name='uyegrupmodel',
            name='uye3',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='uye3', to='calendarapp.uyemodel'),
        ),
        migrations.AddField(
            model_name='uyegrupmodel',
            name='uye4',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='uye4', to='calendarapp.uyemodel'),
        ),
        migrations.AddField(
            model_name='etkinlikmodel',
            name='grup',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='grup', to='calendarapp.uyegrupmodel', verbose_name='Katılımcı Grubu'),
        ),
        migrations.AddField(
            model_name='etkinlikmodel',
            name='kort',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='kort', to='calendarapp.kortmodel', verbose_name='Kort'),
        ),
        migrations.AddField(
            model_name='etkinlikmodel',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='etkinlik', to=settings.AUTH_USER_MODEL, verbose_name='Ekleyen'),
        ),
        migrations.AddField(
            model_name='rezervasyonmodel',
            name='gunler',
            field=models.ManyToManyField(blank=True, null=True, related_name='gunler_rezervasyon_tablosu', to='calendarapp.GunlerModel', verbose_name='Günler'),
        ),
        migrations.AddField(
            model_name='rezervasyonmodel',
            name='saatler',
            field=models.ManyToManyField(blank=True, null=True, related_name='saatler_rezervasyon_tablosu', to='calendarapp.SaatlerModel', verbose_name='Saatler'),
        ),
    ]
