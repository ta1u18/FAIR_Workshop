""" FAIR_Workshop URL Configuration """
from django.urls import path, include
from config import views


urlpatterns = [
    path('', views.index, name='index'),
    path('substances/', include('substances.urls')),
    path('references/', include('references.urls')),
    path('data/', include('data.urls')),
]
