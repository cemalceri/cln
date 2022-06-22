from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def index_kort(request):
    return render(request, "calendarapp/kort/index.html")


@login_required
def kaydet_kort(request):
    pass


@login_required
def detay_kort(request, id):
    pass
