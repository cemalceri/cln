from django.forms import ModelForm

from calendarapp.models.concrete.kort import KortModel
from calendarapp.models.concrete.uye import UyeModel


class KortKayitForm(ModelForm):
    class Meta:
        model = KortModel
        fields = '__all__'
        exclude = ['created_at', 'is_active', 'is_deleted', 'updated_at', 'user']

    def __init__(self, *args, **kwargs):
        super(KortKayitForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'nope'
            })
