"""Urls du projet."""

from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('acronyme/', views.acronyme_page, name='acronyme'),
]
