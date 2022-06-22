from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def index_uye(request):
    print("index_uye")
    return render(request, "calendarapp/uye/index.html")


@login_required
def kaydet_uye(request):
    pass


@login_required
def detay_uye(request, id):
    pass
