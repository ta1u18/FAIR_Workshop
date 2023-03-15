""" views file for the FAIR Workshop data app """
from django.shortcuts import render
from django.http import JsonResponse
from config.models import *
from data.functions import getscidata


def view(request, subid, refid):
    data = {}
    sub = {}
    ref = {}
    return render(request, "../templates/data/view.html", {'data': data, 'sub': sub, 'ref': ref})


def json(request, subid, refid):
    output = {}
    return JsonResponse(output, safe=False)


def scidata(request, subid, refid):
    output = {}
    return JsonResponse(output, safe=False)
