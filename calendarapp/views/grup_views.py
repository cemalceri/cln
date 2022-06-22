from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def index_grup(request):
    return render(request, "calendarapp/grup/index.html")


@login_required
def detay_grup(request, id):
    pass
