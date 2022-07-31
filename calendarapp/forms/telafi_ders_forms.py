from django import forms
from django.db.models import Q
from django.forms import ModelForm

from calendarapp.models.concrete.etkinlik import EtkinlikModel
from calendarapp.models.concrete.telafi_ders import TelafiDersModel
from calendarapp.models.concrete.uye import UyeModel


class TelafiDersKayitForm(ModelForm):
    class Meta:
        model = TelafiDersModel
        fields = '__all__'
        exclude = ['created_at', 'is_active', 'is_deleted', 'updated_at', 'user', 'kullanilan_etkinlik']

    def __init__(self, *args, **kwargs):
        super(TelafiDersKayitForm, self).__init__(*args, **kwargs)
        if self.instance:  # Guncelleme ise sadece o elemanları combolara doldur
            etkinlik = EtkinlikModel.objects.filter(pk=self.instance.telafi_etkinlik_id)
            self.fields["uye"].queryset = UyeModel.objects.filter(pk=self.instance.uye_id)
        else:  # yeni kayıt ise uye combosu ilgili bütün uyeleri doldur.
            etkinlik = EtkinlikModel.objects.filter(pk=self.data['etkinlik_id'])
            self.fields["uye"].queryset = etkinlik.first().grup.grup_uyegrup_relations.all()
        self.fields["telafi_etkinlik"].queryset = etkinlik

        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'nope'
            })
