from django.forms import ModelForm

from calendarapp.models.concrete.uye import UyeModel, UyeGrupModel


class UyeKayitForm(ModelForm):
    class Meta:
        model = UyeModel
        fields = '__all__'
        exclude = ['created_at', 'is_active', 'is_deleted', 'updated_at', 'user']

    def __init__(self, *args, **kwargs):
        super(UyeKayitForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'nope'
            })
        # self.fields["baslangic_tarih_saat"].input_formats = ("%Y-%m-%dT%H:%M",)
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
