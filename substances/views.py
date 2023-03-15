""" view file for the substances app """
from django.shortcuts import render
from config.models import *


def index(request):
    subs = Substances.objects.all().order_by('name')
    return render(request, "../templates/substances/index.html", {'subs': subs})


def view(request, subid):
    sub = Substances.objects.get(id=subid)
    refids = Data.objects.filter(substance_id=sub.id).values_list('reference_id')
    refs = References.objects.filter(id__in=refids)
    return render(request, "../templates/substances/view.html", {'sub': sub, 'refs': refs})