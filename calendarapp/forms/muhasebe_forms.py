from django.forms import ModelForm, DateInput
from calendarapp.models.Enums import AbonelikTipiEnum
from calendarapp.models.concrete.muhasebe import ParaHareketiModel, UcretTarifesiModel
from calendarapp.models.concrete.uye import UyeModel


class UyeParaHareketiKayitForm(ModelForm):
    class Meta:
        model = ParaHareketiModel
        fields = ["uye", "hareket_turu", "ucret_turu", "tutar", "tarih", "aciklama"]
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
        if self.initial.get('uye'):
            self.fields['uye'].queryset = UyeModel.objects.filter(
            pk=self.initial.get('uye'))


class UcretTarifesiKayitForm(ModelForm):
    class Meta:
        model = UcretTarifesiModel
        fields = "__all__"
        exclude = ['created_at', 'is_active', 'is_deleted', 'updated_at', 'user']

    def __init__(self, *args, **kwargs):
        super(UcretTarifesiKayitForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'nope'
            })

    def clean(self):
        abonelik_tipi = self.cleaned_data.get("abonelik_tipi")
        ders_sayisi = self.cleaned_data.get("ders_sayisi")
        if abonelik_tipi != AbonelikTipiEnum.Aidat.name and (ders_sayisi is None or ders_sayisi < 1):
            self.add_error("ders_sayisi", "Abonelik tipi aidat değilse ders sayısı girilmelidir.")
