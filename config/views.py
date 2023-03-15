""" view file for the homepage of the FAIR Workshop website """
from django.shortcuts import render


def index(request):
    return render(request, "../templates/home.html")
