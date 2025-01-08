from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, ID, KEYWORD
from whoosh.qparser import QueryParser, MultifieldParser
from apps.home.models import Recipe, Author, Category
import os


def create_recipe_schema():
    return Schema(
        id=ID(stored=True, unique=True),               # ID único para identificar cada receta
        title=TEXT(stored=True),                       # Título de la receta (búsqueda de texto completo)
        author=TEXT(stored=True),                      # Nombre del autor (búsqueda de texto)
        category=TEXT(stored=True),                    # Nombre de la categoría (búsqueda de texto)
        program=TEXT(stored=True),                     # Programa asociado (si aplica)
        time=TEXT(stored=True),                        # Tiempo estimado de la receta
        difficulty=TEXT(stored=True),                  # Dificultad de la receta
        servings=TEXT(stored=True),                    # Número de comensales
        ingredients=TEXT(stored=True),                 # Lista de ingredientes (búsqueda de texto completo)
        steps=TEXT(stored=True),                       # Pasos de la receta (búsqueda de texto completo)
        tags=KEYWORD(stored=True, commas=True),        # Tags (permiten búsqueda por palabras clave)
        image_url=TEXT(stored=True)                    # URL o ruta de la imagen
    )
  
  
def get_or_create_index():
    index_dir = "whoosh_index"
    if not os.path.exists(index_dir):
        os.mkdir(index_dir)
        schema = create_recipe_schema()
        return create_in(index_dir, schema)
    return open_dir(index_dir)


def search_recipes(query):
    ix = get_or_create_index()
    with ix.searcher() as searcher:
        parser = MultifieldParser(["title", "ingredients", "tags"], ix.schema)
        query = parser.parse(query)
        results = searcher.search(query, limit=10)  # Limita los resultados a 10
        unique_results = {r["id"]: r for r in results}  # Elimina duplicados usando un diccionario
        return [{
            "id": r["id"],
            "title": r["title"],
            "author": r["author"],
            "category": r["category"],
            "time": r["time"],
            "difficulty": r["difficulty"],
            "image_url": r["image_url"]
        } for r in unique_results.values()]