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


@login_required(login_url="/login/")
def scrape_start(request):
    if request.method == "POST":
        try:
            categories = [
                "arroz-con-leche",
                "bizcochos",
                "chocolate",
                "crepes-y-tortitas",
                "cupcakes",
                "desayunos",
                "flanes",
                "galletas",
                "helados-y-sorbetes",
                "magdalenas-y-muffins",
                "meriendas",
                "natillas",
                "postres",
                "postres-tradicionales",
                "tartaletas-y-hojaldres",
                "tartas"
            ]
            scrape_and_save_by_category(categories)
            count = Receta.objects.count()
            return JsonResponse({"success": True, "message": f"{count} recetas cargadas"})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=500)
    else:
        return JsonResponse({"success": False, "message": "Método no permitido"}, status=405)


@login_required(login_url="/login/")
def scrape_status(request):
    if request.method == "GET":
        context = {}
        html_template = loader.get_template('recetas/list.html')
        return HttpResponse(html_template.render(context, request))
    else:
        return JsonResponse({"success": False, "message": "Método no permitido"}, status=405)
