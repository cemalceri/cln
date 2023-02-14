from django import forms
from django.forms import ModelForm, DateInput

from calendarapp.models.Enums import UyeTipiEnum
from calendarapp.models.concrete.uye import UyeModel, UyeGrupModel


class UyeKayitForm(ModelForm):
    uye_tipi = forms.IntegerField(widget=forms.HiddenInput(), initial=UyeTipiEnum.Yetişkin.value)

    class Meta:
        model = UyeModel
        fields = '__all__'
        exclude = ['created_at', 'is_active', 'is_deleted', 'updated_at', 'user', 'uye_no', 'okul', 'veli_telefon',
                   'veli_adi_soyadi']
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
        fields = '__all__'
        exclude = ['created_at', 'is_active', 'is_deleted', 'updated_at', 'user', 'uye_no', 'uye_tipi']
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
