""" urls for the substances app """
from django.urls import path
from substances import views


urlpatterns = [
    path("", views.index, name='substances index'),
    path("view/<subid>", views.view, name='substance view'),

]
