from django.forms import ModelForm

from calendarapp.models.concrete.antrenor import AntrenorModel
from calendarapp.models.concrete.muhasebe import ParaHareketiModel


class ParaHareketiKayitForm(ModelForm):
    class Meta:
        model = ParaHareketiModel
        fields = '__all__'
        exclude = ['created_at', 'is_active', 'is_deleted', 'updated_at', 'user']

    def __init__(self, *args, **kwargs):
        super(ParaHareketiKayitForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'nope'
            })
