from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

from calendarapp.forms.antrenor_forms import AntrenorKayitForm
from calendarapp.forms.muhasebe_forms import ParaHareketiKayitForm
from calendarapp.models.Enums import ParaHareketTuruEnum
from calendarapp.models.concrete.antrenor import AntrenorModel
from calendarapp.models.concrete.muhasebe import ParaHareketiModel
from calendarapp.utils import formErrorsToText


@login_required
def index(request):
    form = ParaHareketiModel.objects.all().order_by('id')
    return render(request, "calendarapp/muhasebe/index.html", {"list": form})


@login_required
def kaydet_uye_odemesi_ajax(request):
    form = ParaHareketiKayitForm(request.POST)
    # form.hareket_turu = ParaHareketTuruEnum.Giris
    print(str(ParaHareketTuruEnum.Giris.value()))
    print(form.hareket_turu)
    if form.is_valid():
        if form.cleaned_data["pk"] and form.cleaned_data["pk"] > 0:
            form = ParaHareketiKayitForm(data=request.POST,
                                         instance=ParaHareketiModel.objects.get(id=form.cleaned_data["pk"]))
            form.save()
        else:
            item = form.save(commit=False)
            item.user = request.user
            item.save()
        return JsonResponse(data={"status": "success", "message": "İşlem Başarılı."})
    else:
        return JsonResponse(data={"status": "error", "message": formErrorsToText(form.errors, ParaHareketiModel)})


@login_required
def detay_antrenor(request, id):
    pass


@login_required
def sil_uye_odemesi(request, id):
    ParaHareketiModel.objects.filter(pk=id).first().delete()
    messages.success(request, "Kayıt Silindi.")
    return redirect("calendarapp:index_muhasebe")
