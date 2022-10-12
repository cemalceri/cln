# Generated by Django 3.2.3 on 2022-10-12 16:40

import calendarapp.models.Enums
import calendarapp.models.concrete.uye
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AbonelikModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('baslangic_tarihi', models.DateField(verbose_name='Başlangıç Tarihi')),
                ('bitis_tarihi', models.DateField(blank=True, null=True, verbose_name='Bitiş Tarihi')),
                ('aktif_mi', models.BooleanField(default=True)),
                ('aciklama', models.TextField(blank=True, null=True, verbose_name='Açıklama')),
            ],
            options={
                'verbose_name': 'Abonelik',
                'verbose_name_plural': 'Abonelik',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='AntrenorModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('adi', models.CharField(max_length=250, verbose_name='Adı')),
                ('renk', models.CharField(choices=[('red', 'Kırmızı'), ('blue', 'Mavi'), ('yellow', 'Sarı'), ('green', 'Yeşil')], default='gray', max_length=20, verbose_name='Renk')),
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
                ('tekrar', models.IntegerField(blank=True, null=True, verbose_name='Tekrar Sayısı')),
                ('aciklama', models.CharField(blank=True, max_length=500, null=True, verbose_name='Açıklama')),
                ('ilk_etkinlik_id', models.IntegerField(blank=True, null=True, verbose_name='İlk Etkinlik ID')),
                ('tamamlandi_mi', models.BooleanField(default=False, verbose_name='Tamamlandı mı?')),
                ('antrenor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='anternor', to='calendarapp.antrenormodel', verbose_name='Antrenör')),
            ],
            options={
                'verbose_name': 'Etkinlik',
                'verbose_name_plural': 'Etkinlikler',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='GrupModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('adi', models.CharField(blank=True, max_length=250, null=True, verbose_name='Adı')),
                ('tekil_mi', models.BooleanField(default=False, verbose_name='Tekil Mi')),
            ],
            options={
                'verbose_name': 'Gruplar',
                'verbose_name_plural': 'Gruplar',
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
            name='OkulModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('adi', models.CharField(max_length=250, verbose_name='Adı')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='okul', to=settings.AUTH_USER_MODEL, verbose_name='Ekleyen')),
            ],
            options={
                'verbose_name': 'Okul',
                'verbose_name_plural': 'Okul',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='PaketModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('adi', models.CharField(max_length=200, verbose_name='Paket Adı')),
                ('tipi', models.SmallIntegerField(choices=[(1, 'Paket'), (2, 'Uyelik')], default=calendarapp.models.Enums.AbonelikTipikEnum['Uyelik'], verbose_name='Tipi')),
                ('adet', models.IntegerField(blank=True, null=True, verbose_name='Adet')),
                ('toplam_fiyati', models.IntegerField(blank=True, null=True, verbose_name='Toplam Fiyatı')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='paket', to=settings.AUTH_USER_MODEL, verbose_name='Ekleyen')),
            ],
            options={
                'verbose_name': 'Paket ve Abonelik Çeşitleri',
                'verbose_name_plural': 'Paket ve Abonelik Çeşitleri',
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
            name='UyeModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('adi', models.CharField(max_length=250, verbose_name='Adı')),
                ('soyadi', models.CharField(max_length=250, verbose_name='Soyadı')),
                ('dogum_tarihi', models.DateField(blank=True, null=True, verbose_name='Doğum Tarihi')),
                ('uye_no', models.IntegerField(default=calendarapp.models.concrete.uye.uye_no_uret, verbose_name='Üye No')),
                ('kimlikNo', models.CharField(blank=True, max_length=11, null=True, verbose_name='KimlikNo')),
                ('telefon', models.CharField(blank=True, max_length=11, null=True, verbose_name='Telefon')),
                ('email', models.EmailField(blank=True, max_length=250, null=True, verbose_name='E-Mail')),
                ('adres', models.TextField(blank=True, max_length=250, null=True, verbose_name='Adres')),
                ('seviye_rengi', models.CharField(choices=[('red', 'Kırmızı'), ('orange', 'Turuncu'), ('green', 'Yeşil'), ('yellow', 'Sarı')], default='gray', max_length=20, verbose_name='Seviye Rengi')),
                ('onaylandi_mi', models.BooleanField(default=False, verbose_name='Onay Durumu')),
                ('aktif_mi', models.BooleanField(default=True, verbose_name='Aktif mi')),
                ('okul', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='okul', to='calendarapp.okulmodel')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='uye', to=settings.AUTH_USER_MODEL, verbose_name='Ekleyen')),
            ],
            options={
                'verbose_name': 'Müşteri',
                'verbose_name_plural': 'Müşteriler',
                'ordering': ['-id'],
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
                ('odeme_sekli', models.SmallIntegerField(blank=True, choices=[(1, 'Ortak_Odeme'), (2, 'Bireysel_Odeme')], null=True, verbose_name='Ödeme Şekli')),
                ('grup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grup_uyegrup_relations', to='calendarapp.grupmodel')),
                ('uye', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='uye_uyegrup_relations', to='calendarapp.uyemodel')),
            ],
            options={
                'verbose_name': 'Üye Grubu',
                'verbose_name_plural': 'Üye Gruplar',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='TelafiDersModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('aciklama', models.TextField(blank=True, null=True, verbose_name='Açıklama')),
                ('kullanilan_etkinlik', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='kullanilanDers', to='calendarapp.etkinlikmodel', verbose_name='Kullanılan Etkinlik')),
                ('telafi_etkinlik', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='telafiDers', to='calendarapp.etkinlikmodel', verbose_name='Etkinlik')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='telafiDers', to=settings.AUTH_USER_MODEL, verbose_name='Ekleyen')),
                ('uye', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='telafiDers', to='calendarapp.uyemodel', verbose_name='Üye')),
            ],
            options={
                'verbose_name': 'Antrenor',
                'verbose_name_plural': 'Antrenor',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='RezervasyonModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('onem_derecesi', models.IntegerField(default=0, verbose_name='Önem Derecesi')),
                ('aktif_mi', models.BooleanField(default=True, verbose_name='Aktif Mi')),
                ('aciklama', models.TextField(blank=True, null=True, verbose_name='Açıklama')),
                ('antrenor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='antrenor', to='calendarapp.antrenormodel')),
                ('gunler', models.ManyToManyField(blank=True, null=True, related_name='gunler_rezervasyon_tablosu', to='calendarapp.GunlerModel', verbose_name='Günler')),
                ('saatler', models.ManyToManyField(blank=True, null=True, related_name='saatler_rezervasyon_tablosu', to='calendarapp.SaatlerModel', verbose_name='Saatler')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rezervasyon', to=settings.AUTH_USER_MODEL, verbose_name='Ekleyen')),
                ('uye', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rezervasyonlar', to='calendarapp.uyemodel')),
            ],
            options={
                'verbose_name': 'Rezervasyon',
                'verbose_name_plural': 'Rezervasyon',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='ParaHareketiModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('tutar', models.DecimalField(decimal_places=2, max_digits=10, max_length=20, verbose_name='Tutar')),
                ('hareket_turu', models.SmallIntegerField(blank=True, choices=[(1, 'Giris'), (2, 'Cikis')], null=True)),
                ('tarih', models.DateField(verbose_name='Tarih')),
                ('aciklama', models.CharField(blank=True, max_length=250, null=True, verbose_name='Açıklama')),
                ('antrenor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='antrenor_parahareketi_relations', to='calendarapp.antrenormodel')),
                ('paket', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='paket_parahareketi_relations', to='calendarapp.paketmodel')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_parahareketi_relations', to=settings.AUTH_USER_MODEL)),
                ('uye', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='uye_parahareketi_relations', to='calendarapp.uyemodel')),
            ],
            options={
                'verbose_name': 'Para Hareketleri',
                'verbose_name_plural': 'Para Hareketleri',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='PaketKullanimModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('abonelik', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calendarapp.abonelikmodel', verbose_name='Abonelik')),
                ('etkinlik', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calendarapp.etkinlikmodel', verbose_name='Etkinlik')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='paket_kullanim', to=settings.AUTH_USER_MODEL, verbose_name='Ekleyen')),
                ('uye', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calendarapp.uyemodel', verbose_name='Üye')),
            ],
            options={
                'verbose_name': 'Paket Kullanım',
                'verbose_name_plural': 'Paket Kullanım',
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
        migrations.AddField(
            model_name='etkinlikmodel',
            name='grup',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='etkinlik_grup_relations', to='calendarapp.grupmodel', verbose_name='Katılımcı Grubu'),
        ),
        migrations.AddField(
            model_name='etkinlikmodel',
            name='kort',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='kort', to='calendarapp.kortmodel', verbose_name='Kort'),
        ),
        migrations.AddField(
            model_name='etkinlikmodel',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='etkinlik', to=settings.AUTH_USER_MODEL, verbose_name='Ekleyen'),
        ),
        migrations.CreateModel(
            name='EtkinlikKatilimModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('katilim_durumu', models.SmallIntegerField(choices=[(1, 'Katıldı'), (2, 'Katılmadı'), (3, 'İptal')], default=1, verbose_name='Katılım Durumu')),
                ('etkinlik', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='etkinlik', to='calendarapp.etkinlikmodel', verbose_name='Etkinlik')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='etkinlik_katilim', to=settings.AUTH_USER_MODEL, verbose_name='Ekleyen')),
                ('uye', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='uye', to='calendarapp.uyemodel', verbose_name='Üye')),
            ],
            options={
                'verbose_name': 'Etkinlik Katılım',
                'verbose_name_plural': 'Etkinlik Katılımları',
                'ordering': ['-id'],
            },
        ),
        migrations.AddField(
            model_name='abonelikmodel',
            name='paket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='calendarapp.paketmodel', verbose_name='Paket'),
        ),
        migrations.AddField(
            model_name='abonelikmodel',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='abonelik', to=settings.AUTH_USER_MODEL, verbose_name='Ekleyen'),
        ),
        migrations.AddField(
            model_name='abonelikmodel',
            name='uye',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calendarapp.uyemodel', verbose_name='Üye'),
        ),
    ]
