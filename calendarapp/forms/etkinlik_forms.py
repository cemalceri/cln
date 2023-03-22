from django.forms import ModelForm, DateInput
from django import forms
from calendarapp.models.concrete.etkinlik import EtkinlikModel, HaftalikPlanModel


class EtkinlikForm(ModelForm):
    pk = forms.IntegerField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = EtkinlikModel
        fields = '__all__'
        exclude = ['tamamlandi_uye', 'tamamlandi_antrenor', 'tamamlandi_yonetici', 'ilk_etkinlik_id',
                   'haftalik_plan_kodu', 'iptal_mi', 'iptal_eden', 'iptal_tarih_saat', 'created_at',
                   'is_active', 'is_deleted', 'updated_at', 'user', 'paket_id']
        # datetime-local is a HTML5 input type
        widgets = {
            "baslangic_tarih_saat": DateInput(
                attrs={"type": "datetime-local", "class": "form-control"},
                format="%Y-%m-%dT%H:%M",
            ),
            "bitis_tarih_saat": DateInput(
                attrs={"type": "datetime-local", "class": "form-control"},
                format="%Y-%m-%dT%H:%M",
            ),
        }
        help_texts = {
            # "tekrar": '*Girilen sayı kadar sonraki haftalara kayıt oluşturulur.',
        }

    def __init__(self, *args, **kwargs):
        super(EtkinlikForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
            })
        self.fields["grup"].widget.attrs.update({
            'class': 'select2', })
        # self.fields["bitis_tarih_saat"].input_formats = ("%Y-%m-%dT%H:%M",)

    def clean(self):
        baslangic_tarih_saat = self.cleaned_data.get("baslangic_tarih_saat")
        bitis_tarih_saat = self.cleaned_data.get("bitis_tarih_saat")
        if baslangic_tarih_saat > bitis_tarih_saat:
            self.add_error('bitis_tarih_saat', "Bitiş tarihi başlangıç tarihinden önce olamaz.")
        elif baslangic_tarih_saat == bitis_tarih_saat:
            self.add_error('bitis_tarih_saat', "Bitiş tarihi başlangıç tarihine eşit olamaz.")
        if baslangic_tarih_saat.minute % 30 != 0:
            self.add_error('baslangic_tarih_saat', "Başlangıç saati 30 dakikanın katları olmalıdır.")
        if bitis_tarih_saat.minute % 30 != 0:
            self.add_error('bitis_tarih_saat', "Bitiş saati 30 dakikanın katları olmalıdır.")
        return self.cleaned_data


class HaftalikPlanForm(ModelForm):
    pk = forms.IntegerField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = HaftalikPlanModel
        fields = '__all__'
        exclude = ['kod', 'created_at', 'is_active', 'is_deleted', 'updated_at', 'user']
        # datetime-local is a HTML5 input type
        widgets = {
            "baslangic_tarih_saat": DateInput(
                attrs={"type": "datetime-local", "class": "form-control"},
                format="%Y-%m-%dT%H:%M",
            ),
            "bitis_tarih_saat": DateInput(
                attrs={"type": "datetime-local", "class": "form-control"},
                format="%Y-%m-%dT%H:%M",
            ),
            "ders_baslangic_tarihi": DateInput(
                attrs={"type": "date", "class": "form-control"},
                format="%Y-%m-%d",
            ),
        }
        help_texts = {
            # "tekrar": '*Girilen sayı kadar sonraki haftalara kayıt oluşturulur.',
        }

    def __init__(self, *args, **kwargs):
        super(HaftalikPlanForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
            })
        self.fields["grup"].widget.attrs.update({'class': 'select2'})
        # self.fields["baslangic_tarih_saat"].input_formats = ("%Y-%m-%dT%H:%M",)
        # self.fields["bitis_tarih_saat"].input_formats = ("%Y-%m-%dT%H:%M",)
