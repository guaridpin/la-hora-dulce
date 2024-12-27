# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import json
from django.http import JsonResponse
from apps.scraper.utils import scrape_and_save_by_category
from .models import Receta
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


def scrape_view(request):
    if request.method == "POST":  # Asegúrate de usar POST para realizar esta acción
        categories = [
            "arroz-con-leche",
            "tartas",
            "bizcochos",
            "ensaladas",
            "sopas"
        ]
        # Llamar al método de scraping
        scrape_and_save_by_category(categories)
        
        # Contar cuántas recetas se cargaron
        count = Receta.objects.count()
        return JsonResponse({"success": True, "message": f"{count} recetas cargadas"})
    else:
        return JsonResponse({"success": False, "message": "Método no permitido"}, status=405)
