from django.forms import ModelForm, DateInput
from calendarapp.models.concrete.abonelik import UyePaketModel


class UyePaketKayitForm(ModelForm):
    class Meta:
        model = UyePaketModel
        fields = '__all__'
        exclude = ['created_at', 'is_active', 'is_deleted', 'updated_at', 'user']
        widgets = {
            "baslangic_tarihi": DateInput(
                attrs={"type": "date", "class": "form-control"},
                format="%Y-%m-%d",
            ),
            "bitis_tarihi": DateInput(
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
