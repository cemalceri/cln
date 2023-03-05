from django.forms import ModelForm

from calendarapp.models.concrete.antrenor import AntrenorModel
from calendarapp.models.concrete.commons import OkulModel


class OkulKayitForm(ModelForm):
    class Meta:
        model = OkulModel
        fields = '__all__'
        exclude = ['created_at', 'is_active', 'is_deleted', 'updated_at', 'user']

    def __init__(self, *args, **kwargs):
        super(OkulKayitForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'nope'
            })
