# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from .models import Receta, Autor, Categoria

# Register your models here.
admin.site.register(Autor)
admin.site.register(Categoria)
admin.site.register(Receta)