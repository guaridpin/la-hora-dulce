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
    path('search/', views.search_view, name='search'),
    path('recipe/<path:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path("filter-ingredients/", views.filter_by_ingredients, name="filter_by_ingredients"),
    path("filter-categories/", views.filter_by_category, name="filter_by_category"),
    path("filter-time-difficulty/", views.filter_by_time_and_difficulty, name="filter_by_time_and_difficulty"),
    re_path(r'^.*\.*', views.pages, name='pages'),
]

