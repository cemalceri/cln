from django.forms import ModelForm, DateInput
from django import forms
from calendarapp.models.concrete.rezervasyon import RezervasyonModel
from calendarapp.models.member.rezervasyon_member import RezervasyonMember


class RezervasyonForm(ModelForm):
    pk = forms.IntegerField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = RezervasyonModel
        fields = ["baslik", "aciklama", "baslangic_tarih_saat", "bitis_tarih_saat"]
        # datetime-local is a HTML5 input type
        widgets = {
            "baslik": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter event title"}
            ),
            "aciklama": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter event description",
                }
            ),
            "baslangic_tarih_saat": DateInput(
                attrs={"type": "datetime-local", "class": "form-control"},
                format="%Y-%m-%dT%H:%M",
            ),
            "bitis_tarih_saat": DateInput(
                attrs={"type": "datetime-local", "class": "form-control"},
                format="%Y-%m-%dT%H:%M",
            ),
        }
        exclude = ["user"]

    def __init__(self, *args, **kwargs):
        super(RezervasyonForm, self).__init__(*args, **kwargs)
        # input_formats to parse HTML5 datetime-local input to datetime field
        self.fields["baslangic_tarih_saat"].input_formats = ("%Y-%m-%dT%H:%M",)
        self.fields["bitis_tarih_saat"].input_formats = ("%Y-%m-%dT%H:%M",)

# class AddMemberForm(forms.ModelForm):
#     class Meta:
#         model = RezervasyonMember
#         fields = ["user"]
