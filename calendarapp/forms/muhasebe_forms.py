from django import forms
from django.forms import ModelForm, DateInput

from calendarapp.models.concrete.antrenor import AntrenorModel
from calendarapp.models.concrete.muhasebe import ParaHareketiModel


class UyeParaHareketiKayitForm(ModelForm):
    class Meta:
        model = ParaHareketiModel
        fields = ["uye", "hareket_turu", "odeme_turu", "tutar", "tarih", "aciklama"]
        # exclude = ['created_at', 'is_active', 'is_deleted', 'updated_at', 'user']
        widgets = {
            "tarih": DateInput(
                attrs={"type": "date", "class": "form-control"},
                format="%Y-%m-%d",
            ),
        }

    def __init__(self, *args, **kwargs):
        super(UyeParaHareketiKayitForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'nope'
            })
