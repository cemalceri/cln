from django import forms
from django.forms import ModelForm

from calendarapp.models.Enums import GunlerModel, SaatlerModel
from calendarapp.models.concrete.rezervasyon import RezervasyonModel


class RezervasyonKayitForm(ModelForm):
    gunler = forms.ModelMultipleChoiceField(widget=forms.SelectMultiple, queryset=GunlerModel.objects.all(),
                                            help_text="*Gün seçilmez ise bütün günler geçerlidir.", required=False)
    saatler = forms.ModelMultipleChoiceField(widget=forms.SelectMultiple, queryset=SaatlerModel.objects.all(),
                                             help_text="*Saat seçilmez ise bütün saatler geçerlidir." ,required=False)

    class Meta:
        model = RezervasyonModel
        fields = '__all__'
        exclude = ['created_at', 'is_active', 'is_deleted', 'updated_at', 'user']

    def __init__(self, *args, **kwargs):
        super(RezervasyonKayitForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'nope'
            })

