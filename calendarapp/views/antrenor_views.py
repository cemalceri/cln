from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def index_antrenor(request):
    return render(request, "calendarapp/antrenor/index.html")


@login_required
def kaydet_antrenor(request):
    pass


@login_required
def detay_antrenor(request, id):
    pass
