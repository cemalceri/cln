from django import forms
from django.db.models import Q
from django.forms import ModelForm, DateInput

from calendarapp.models.concrete.etkinlik import EtkinlikModel
from calendarapp.models.concrete.telafi_ders import TelafiDersModel
from calendarapp.models.concrete.uye import UyeModel


class TelafiDersKayitForm(ModelForm):
    class Meta:
        model = TelafiDersModel
        fields = '__all__'
        exclude = ['created_at', 'is_active', 'is_deleted', 'updated_at', 'user', 'kullanilan_etkinlik',
                   'telafi_etkinlik', 'yapilan_kort', 'yapilan_antrenor', 'yapilma_tarih_saat', 'yapilma_aciklama']

    def __init__(self, *args, **kwargs):
        super(TelafiDersKayitForm, self).__init__(*args, **kwargs)
        print(self.initial.get('uye'))
        if self.initial.get('uye'):
            self.fields['uye'].queryset = self.initial.get('uye')
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'nope'
            })


class TelafiDersGetirForm(ModelForm):
    class Meta:
        model = TelafiDersModel
        fields = '__all__'
        exclude = ['created_at', 'is_active', 'is_deleted', 'updated_at', 'user', 'kullanilan_etkinlik',
                   'telafi_etkinlik', 'yapilan_kort', 'yapilan_antrenor', 'yapilma_tarih_saat', 'yapilma_aciklama']

    def __init__(self, *args, **kwargs):
        super(TelafiDersGetirForm, self).__init__(*args, **kwargs)
        etkinlik = EtkinlikModel.objects.filter(pk=self.data["etkinlik_id"])
        self.fields["uye"] = forms.ModelChoiceField(widget=forms.Select,
                                                    queryset=etkinlik.first().grup.grup_uyegrup_relations.all(),
                                                    initial=0)

        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'nope'
            })


class TelafiDersGuncelleForm(ModelForm):
    class Meta:
        model = TelafiDersModel
        fields = '__all__'
        exclude = ['created_at', 'is_active', 'is_deleted', 'updated_at', 'user', 'kullanilan_etkinlik',
                   'telafi_etkinlik', 'yapilan_kort', 'yapilan_antrenor', 'yapilma_tarih_saat', 'yapilma_aciklama']

    def __init__(self, *args, **kwargs):
        super(TelafiDersGuncelleForm, self).__init__(*args, **kwargs)
        # self.fields["uye"].queryset = etkinlik.first().grup.grup_uyegrup_relations.all()
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'nope'
            })


class YapilanTelafiDersForm(ModelForm):
    class Meta:
        model = TelafiDersModel
        fields = '__all__'
        exclude = ['created_at', 'is_active', 'is_deleted', 'updated_at', 'user', 'telafi_etkinlik',
                   'uye', 'aciklama']

        widgets = {
            "yapilma_tarih_saat": DateInput(
                attrs={"type": "datetime-local", "class": "form-control", "required": "required"},
                format="%d-%m-%YT%H:%M",
            )}

    def __init__(self, *args, **kwargs):
        super(YapilanTelafiDersForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'nope'
            })
