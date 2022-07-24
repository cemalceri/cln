from django.forms import ModelForm

from calendarapp.models.concrete.antrenor import AntrenorModel


class AntrenorKayitForm(ModelForm):
    class Meta:
        model = AntrenorModel
        fields = '__all__'
        exclude = ['created_at', 'is_active', 'is_deleted', 'updated_at', 'user']

    def __init__(self, *args, **kwargs):
        super(AntrenorKayitForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'nope'
            })
