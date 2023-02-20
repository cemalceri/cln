from django import forms
from django.forms import ModelForm, DateInput

from calendarapp.models.Enums import UyeTipiEnum
from calendarapp.models.concrete.uye import UyeModel, UyeGrupModel


class UyeKayitForm(ModelForm):
    uye_tipi = forms.IntegerField(widget=forms.HiddenInput(), initial=UyeTipiEnum.Yetişkin.value)

    class Meta:
        model = UyeModel
        fields = ['adi', 'soyadi', 'kimlik_no', 'cinsiyet', 'dogum_tarihi', 'dogum_yeri', 'adres', 'telefon', 'email',
                  'meslek', 'seviye_rengi', 'onaylandi_mi', 'aktif_mi', 'referansi', 'tenis_gecmisi_var_mi',
                  'program_tercihi', 'gunler', 'saatler', ]
        widgets = {
            "dogum_tarihi": DateInput(
                attrs={"type": "date", "class": "form-control"},
                format="%Y-%m-%d",
            ),
        }

    def __init__(self, *args, **kwargs):
        super(UyeKayitForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'nope'
            })


class GencUyeKayitForm(ModelForm):
    uye_tipi = forms.IntegerField(widget=forms.HiddenInput(), initial=UyeTipiEnum.Genç.value)

    class Meta:
        model = UyeModel
        fields = ['adi', 'soyadi', 'kimlik_no', 'cinsiyet', 'dogum_tarihi', 'dogum_yeri', 'adres', 'telefon', 'email',
                  'seviye_rengi', 'onaylandi_mi', 'aktif_mi', 'referansi', 'tenis_gecmisi_var_mi', 'program_tercihi',
                  'gunler', 'saatler', 'anne_adi_soyadi', 'anne_telefon', 'anne_mail', 'anne_meslek', 'baba_adi_soyadi',
                  'baba_telefon', 'baba_telefon', 'baba_meslek', 'okul']
        widgets = {
            "dogum_tarihi": DateInput(
                attrs={"type": "date", "class": "form-control"},
                format="%Y-%m-%d",
            ),
        }

    def __init__(self, *args, **kwargs):
        super(GencUyeKayitForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'nope'
            })
        self.fields["uye_tipi"].initial = UyeTipiEnum.Genç.value
        # self.fields["bitis_tarih_saat"].input_formats = ("%Y-%m-%dT%H:%M",)


class UyeGrupKayitForm(ModelForm):
    class Meta:
        model = UyeGrupModel
        fields = '__all__'
        exclude = ['uye_no', 'created_at', 'is_active', 'is_deleted', 'updated_at', 'user']

    def __init__(self, *args, **kwargs):
        super(UyeGrupKayitForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'nope'
            })
