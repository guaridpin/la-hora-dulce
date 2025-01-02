# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('scraping/start/', views.scrape_start, name='scrape_start'),
    path('scraping/status/', views.scrape_status, name='scrape_status'),
     path('search/', views.search_view, name='search'),  # Ruta para la búsqueda
    re_path(r'^.*\.*', views.pages, name='pages'),
]

