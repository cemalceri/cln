from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from calendarapp.forms.antrenor_forms import AntrenorKayitForm
from calendarapp.forms.telafi_ders_forms import TelafiDersKayitForm
from calendarapp.models.concrete.antrenor import AntrenorModel
from calendarapp.models.concrete.etkinlik import EtkinlikModel
from calendarapp.models.concrete.telafi_ders import TelafiDersModel
from calendarapp.models.concrete.uye import UyeGrupModel
from calendarapp.utils import formErrorsToText


@login_required
def index(request):
    form = TelafiDersModel.objects.all().order_by('id')
    return render(request, "calendarapp/telafi_ders/index.html", {"list": form})

@login_required
def getir_grup_bilgisi(request):
    grup_id= request.GET.get('etkinlik_id')
    grup = EtkinlikModel.objects.get(id=grup_id).grup.grup_uyegrup_relations.all()
    print(grup)
    print(grup)
    html = render_to_string('calendarapp/telafi_ders/partials/_kaydet_modal.html', context={'form': grup})
    print(html)
    return JsonResponse(data={'status':'success', 'html': html})

@login_required
def kaydet(request, etkinlik_id=None):
    if request.method == 'POST':
        form = TelafiDersKayitForm(request.POST)
        if form.is_valid():
            entity = form.save(commit=False)
            entity.user = request.user
            entity.save()
            messages.success(request, "Kaydedildi.")
            return redirect("calendarapp:index_telafi_ders")
        else:
            messages.error(request, formErrorsToText(form.errors, TelafiDersModel))
            return render(request, "calendarapp/telafi_ders/kaydet.html",
                          context={'form': form, 'etkinlik_id': etkinlik_id})
    form = TelafiDersKayitForm(data={"etkinlik_id": etkinlik_id})
    return render(request, "calendarapp/telafi_ders/kaydet.html", context={'form': form, 'etkinlik_id': etkinlik_id})


@login_required
def guncelle(request, id=None):
    if request.method == 'POST':
        id = request.POST.get("id")
        entity = TelafiDersModel.objects.filter(pk=id).first()
        form = TelafiDersKayitForm(request.POST, instance=entity)
        if form.is_valid():
            entity = form.save(commit=False)
            entity.save()
            messages.success(request, "Kaydedildi.")
            return redirect("calendarapp:index_telafi_ders")
        else:
            messages.error(request, formErrorsToText(form.errors, TelafiDersModel))
            return render(request, "calendarapp/telafi_ders/kaydet.html", context={'form': form,'etkinlik_id': None})
    form = TelafiDersKayitForm(instance=TelafiDersModel.objects.filter(pk=id).first())
    return render(request, "calendarapp/telafi_ders/kaydet.html", context={'form': form})


@login_required
def detay(request, id):
    pass


@login_required
def sil(request, id):
    TelafiDersModel.objects.filter(pk=id).first().delete()
    messages.success(request, "Kayıt Silindi.")
    return redirect("calendarapp:index_telafi_ders")
