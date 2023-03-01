from django import forms
from django.forms import ModelForm, DateInput

from calendarapp.models.Enums import AbonelikTipiEnum
from calendarapp.models.concrete.abonelik import UyePaketModel
from calendarapp.models.concrete.muhasebe import UcretTarifesiModel


class UyePaketKayitForm(ModelForm):
    class Meta:
        model = UyePaketModel
        fields = '__all__'
        exclude = ['created_at', 'is_active', 'is_deleted', 'updated_at', 'user', 'adet']
        widgets = {
            "baslangic_tarih": DateInput(
                attrs={"type": "date", "class": "form-control"},
                format="%Y-%m-%d",
            ),
            "bitis_tarih": DateInput(
                attrs={"type": "date", "class": "form-control"},
                format="%Y-%m-%d",
            ),
        }

    def __init__(self, *args, **kwargs):
        super(UyePaketKayitForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'nope'
            })
        self.fields['ucret_tarifesi'].queryset = UcretTarifesiModel.objects.filter(
            abonelik_tipi=AbonelikTipiEnum.Paket.name)

    def clean(self):
        grup_mu = self.cleaned_data.get("grup_mu")
        kisi_sayisi = UcretTarifesiModel.objects.get(pk=self.cleaned_data.get("ucret_tarifesi").id).kisi_sayisi
        if grup_mu and kisi_sayisi < 2:
            self.add_error('grup_mu', "Seçilen paket grup paketi değildir. Lütfen grup paketi seçiniz.")
        elif not grup_mu and kisi_sayisi > 1:
            self.add_error('grup_mu', "Seçilen paket grup paketidir. Lütfen başka paket seçiniz.")

# class PaketKayitForm(ModelForm):
#     class Meta:
#         model = PaketModel
#         fields = '__all__'
#         exclude = ['created_at', 'is_active', 'is_deleted', 'updated_at', 'user']
#
#     def __init__(self, *args, **kwargs):
#         super(PaketKayitForm, self).__init__(*args, **kwargs)
#         for field in iter(self.fields):
#             self.fields[field].widget.attrs.update({
#                 'class': 'form-control',
#                 'autocomplete': 'nope'
#             })
