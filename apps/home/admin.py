# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from .models import Recipe, Category, Author

# Register your models here.
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Recipe)