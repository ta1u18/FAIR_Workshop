""" urls for the substances app """
from django.urls import path
from data import views


urlpatterns = [
    path("view/<subid>/<refid>", views.view, name='data view'),
    path("json/<subid>/<refid>", views.json, name='json view'),
    path("scidata/<subid>/<refid>", views.scidata, name='jsonld view'),
]
