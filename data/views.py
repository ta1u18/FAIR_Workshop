""" views file for the FAIR Workshop data app """
from django.shortcuts import render
from django.http import JsonResponse
from config.models import *
from data.functions import getscidata


def view(request, subid, refid):
    data = Data.objects.filter(substance_id=subid, reference_id=refid)
    sub = Substances.objects.get(id=subid)
    ref = References.objects.get(id=refid)
    return render(request, "../templates/data/view.html", {'data': data, 'sub': sub, 'ref': ref})


def json(request, subid, refid):
    data = Data.objects.filter(substance_id=subid, reference_id=refid)
    sub = Substances.objects.get(id=subid)
    ref = References.objects.get(id=refid)
    output = {}
    output.update({'substance': sub.name})
    output.update({'reference': ref.citation})
    output.update({'data': []})
    for datum in data:
       d = {}
       d.update({'value': datum.pka_value})
       d.update({'type': datum.pka_type})
       d.update({'temperature (°C)': datum.temp})
       mtdids = datum.datamethods_set.all().values_list('method_id', flat=True)
       methods = Methods.objects.filter(id__in=mtdids).values_list(datum.source, flat=True)
       d.update({'methods': list(methods)}),
       d.update({'remarks': datum.remarks})
       output['data'].append(d)
    return JsonResponse(output, safe=False)


def scidata(request, subid, refid):
    output = getscidata(subid,refid)
    return JsonResponse(output, safe=False)
