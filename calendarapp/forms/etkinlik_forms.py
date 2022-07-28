from django.forms import ModelForm, DateInput
from django import forms
from calendarapp.models.concrete.etkinlik import EtkinlikModel


class EtkinlikForm(ModelForm):
    pk = forms.IntegerField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = EtkinlikModel
        fields = '__all__'
        exclude = ['tamamlandi_mi','ilk_etkinlik_id', 'created_at', 'is_active', 'is_deleted', 'updated_at', 'user']
        # datetime-local is a HTML5 input type
        widgets = {
            "baslangic_tarih_saat": DateInput(
                attrs={"type": "datetime-local", "class": "form-control"},
                format="%d-%m-%YT%H:%M",
            ),
            "bitis_tarih_saat": DateInput(
                attrs={"type": "datetime-local", "class": "form-control"},
                format="%d-%m-%YT%H:%M",
            ),
        }
        help_texts = {
            "tekrar": '*Girilen sayı kadar sonraki haftalara kayıt oluşturulur.',
        }

    def __init__(self, *args, **kwargs):
        super(EtkinlikForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
            })
        # self.fields["baslangic_tarih_saat"].input_formats = ("%Y-%m-%dT%H:%M",)
        # self.fields["bitis_tarih_saat"].input_formats = ("%Y-%m-%dT%H:%M",)

# class AddMemberForm(forms.ModelForm):
#     class Meta:
#         model = EtkinlikMember
#         fields = ["user"]
