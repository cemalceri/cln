from django.forms import ModelForm

from calendarapp.models.concrete.etkinlik import EtkinlikModel
from calendarapp.models.concrete.telafi_ders import TelafiDersModel


class TelafiDersKayitForm(ModelForm):
    class Meta:
        model = TelafiDersModel
        fields = '__all__'
        exclude = ['created_at', 'is_active', 'is_deleted', 'updated_at', 'user', 'kullanilan_etkinlik']

    def __init__(self, *args, **kwargs):
        super(TelafiDersKayitForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'nope'
            })
        print(self.data["etkinlik_id"])
        etkinlik = EtkinlikModel.objects.first(self.data["etkinlik_id"])
        self.fields["telafi_etkinlik"].queryset = etkinlik
