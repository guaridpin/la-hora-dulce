# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from . import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('scrape/', views.scrape_view, name='scrape'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
