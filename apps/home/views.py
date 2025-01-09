# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import json
from django.http import JsonResponse
from django.shortcuts import render
from apps.scraper.utils import scrape_and_save_by_category, get_or_create_index
from .models import Recipe
from apps.scraper.whoosh_index import search_recipes
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
            count = scrape_and_save_by_category(categories)

            return JsonResponse({"success": True, "message": f"{count} recetas cargadas"})
        except Exception as e:
            print(f"Error en scrape_start: {e}")  # Registro detallado
            return JsonResponse({"success": False, "message": str(e)}, status=500)
    return JsonResponse({"success": False, "message": "Método no permitido"}, status=405)


@login_required(login_url="/login/")
def scrape_status(request):
    if request.method == "GET":
        try:
            ix = get_or_create_index()

            with ix.searcher() as searcher:
                # Contar el número total de recetas indexadas
                total_recipes = searcher.doc_count_all()
                results = searcher.documents()
                
                # Opcional: Si quieres devolver datos adicionales, procesa los documentos
                recipies = [
                    {
                        "id": r["id"],
                        "title": r["title"],
                        "author": r["author"],
                        "category": r["category"],
                        "program": r["program"],
                        "time": r["time"],
                        "difficulty": r["difficulty"],
                        "servings": r["servings"],
                        "ingredients": r["ingredients"],
                        "steps": r["steps"],
                        "tags": r["tags"]
                    } for r in results
                ]
            
            # Pasar el total de recetas indexadas al contexto
            context = {'total_recipes': total_recipes, 'recetas': recipies}
            
            html_template = loader.get_template('recetas/list.html')
            return HttpResponse(html_template.render(context, request))
        except Exception as e:
            print(f"Error en scrape_status: {e}")
            return JsonResponse({"success": False, "message": str(e)}, status=500)
    return JsonResponse({"success": False, "message": "Método no permitido"}, status=405)


@login_required(login_url="/login/")
def search_view(request):
    query = request.GET.get('q', '')
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 10))  # Tamaño de página predeterminado

    if query:
        search_data = search_recipes(query, page=page, page_size=page_size)
        page_numbers = range(1, search_data["total_pages"] + 1)  # Genera la lista de páginas
    else:
        search_data = {"results": [], "total_results": 0, "page": 1, "page_size": page_size, "total_pages": 0}
        page_numbers = []

    return render(request, 'recetas/search_results.html', {
        'query': query,
        'results': search_data["results"],
        'total_results': search_data["total_results"],
        'page': search_data["page"],
        'page_size': search_data["page_size"],
        'total_pages': search_data["total_pages"],
        'page_numbers': page_numbers,  # Añadimos la lista de páginas
    })


@login_required(login_url="/login/")
def recipe_detail(request, recipe_id):
    try:
        ix = get_or_create_index()
        with ix.searcher() as searcher:
            doc = searcher.document(id=recipe_id)
            if not doc:
                return render(request, 'home/page-404.html', {"message": "Receta no encontrada"})

            # Pasar los datos al contexto
            context = {
                "title": doc.get("title"),
                "author": doc.get("author"),
                "category": doc.get("category"),
                "program": doc.get("program"),
                "time": doc.get("time"),
                "difficulty": doc.get("difficulty"),
                "servings": doc.get("servings"),
                "ingredients": doc.get("ingredients"),
                "steps": doc.get("steps"),
                "tags": doc.get("tags"),
                "image_url": doc.get("image_url"),
            }
            return render(request, 'recetas/recipe_detail.html', context)
    except Exception as e:
        return render(request, 'home/page-404.html', {"message": str(e)})
    

# Lista de ingredientes categorizados
INGREDIENTES = {
    "Ingredientes básicos": [
        "Harina", "Azúcar", "Huevos", "Mantequilla", "Aceite vegetal",
        "Leche", "Nata", "Yogur", "Levadura"
    ],
    "Endulzantes y aromatizantes": [
        "Vainilla", "Azúcar glas", "Miel", "Edulcorante"
    ],
    "Cacao y chocolate": ["Cacao", "Chocolate"],
    "Frutas frescas": [
        "Plátano", "Manzana", "Fresas", "Arándanos", "Frambuesas",
        "Cerezas", "Mango", "Limón", "Naranja", "Piña", "Pera", "Boniato"
    ]
}


@login_required(login_url="/login/")
def filter_by_ingredients(request):
    if request.method == "POST":
        # Obtener los ingredientes seleccionados
        selected_ingredients = request.POST.getlist("ingredients")
        query = " OR ".join(selected_ingredients)  # Crear una consulta OR para buscar cualquiera de los ingredientes
        page = int(request.GET.get("page", 1))
        page_size = int(request.GET.get("page_size", 10))

        # Buscar recetas que contengan los ingredientes
        search_data = search_recipes(query, page=page, page_size=page_size)

        return render(request, "recetas/search_results.html", {
            "query": ", ".join(selected_ingredients),
            "results": search_data["results"],
            "total_results": search_data["total_results"],
            "page": search_data["page"],
            "page_size": search_data["page_size"],
            "total_pages": search_data["total_pages"],
        })

    return render(request, "recetas/filter_ingredients.html", {"ingredientes": INGREDIENTES})
