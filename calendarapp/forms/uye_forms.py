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
                  'program_tercihi', 'gunler', 'saatler', 'profil_fotografi']
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
        self.fields["uye_tipi"].initial = UyeTipiEnum.Yetişkin.value

    def clean_profil_fotografi(self):
        profil_fotografi = self.cleaned_data.get("profil_fotografi")
        if profil_fotografi:
            if profil_fotografi.size > 2 * 1024 * 1024:
                raise forms.ValidationError("Dosya boyutu 2MB'dan büyük olamaz.")
            if not profil_fotografi.name.endswith('.jpg'):
                raise forms.ValidationError("Dosya uzantısı .jpg olmalıdır.")
        return profil_fotografi


class GencUyeKayitForm(ModelForm):
    uye_tipi = forms.IntegerField(widget=forms.HiddenInput(), initial=UyeTipiEnum.Sporcu.value)

    class Meta:
        model = UyeModel
        fields = ['adi', 'soyadi', 'kimlik_no', 'cinsiyet', 'dogum_tarihi', 'dogum_yeri', 'adres', 'telefon', 'email',
                  'seviye_rengi', 'onaylandi_mi', 'aktif_mi', 'referansi', 'tenis_gecmisi_var_mi', 'program_tercihi',
                  'gunler', 'saatler', 'anne_adi_soyadi', 'anne_telefon', 'anne_mail', 'anne_meslek', 'baba_adi_soyadi',
                  'baba_telefon', 'baba_telefon', 'baba_meslek', 'okul', 'profil_fotografi']
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
        self.fields["uye_tipi"].initial = UyeTipiEnum.Sporcu.value


    def clean_profil_fotografi(self):
        profil_fotografi = self.cleaned_data.get("profil_fotografi")
        if profil_fotografi:
            if profil_fotografi.size > 2 * 1024 * 1024:
                raise forms.ValidationError("Dosya boyutu 2MB'dan büyük olamaz.")
            if not profil_fotografi.name.endswith('.jpg'):
                raise forms.ValidationError("Dosya uzantısı .jpg olmalıdır.")
        return profil_fotografi


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
