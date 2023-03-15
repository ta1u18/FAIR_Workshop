""" view file for the substances app """
from django.shortcuts import render
from config.models import *


def index(request):
    refs = References.objects.all().order_by('citation')
    return render(request, "../templates/references/index.html", {'refs': refs})


def view(request, refid):
    ref = References.objects.get(id=refid)
    return render(request, "../templates/references/view.html", {'ref': ref})
