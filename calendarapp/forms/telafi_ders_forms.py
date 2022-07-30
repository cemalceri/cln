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
        etkinlik = EtkinlikModel.objects.filter(pk=self.initial["telafi_etkinlik"])
        self.fields["telafi_etkinlik"].queryset = etkinlik
        self.fields["uye"].queryset = UyeModel.objects.filter(
            Q(pk=etkinlik.first().grup.uye1.pk) | Q(pk=etkinlik.first().grup.uye2))
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'nope'
            })
