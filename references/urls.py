""" urls for the substances app """
from django.urls import path
from references import views


urlpatterns = [
    path("", views.index, name='references index'),
    path("view/<refid>", views.view, name='reference view'),

]
