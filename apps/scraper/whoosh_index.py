from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, ID, KEYWORD
from whoosh.qparser import QueryParser, MultifieldParser, OrGroup
from collections import Counter
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


def search_recipes(query, page=1, page_size=10):
    """
    Busca recetas en el índice con paginación.
    
    :param query: La consulta de búsqueda.
    :param page: El número de página actual.
    :param page_size: El número de resultados por página.
    :return: Un diccionario con los resultados paginados y metadatos.
    """
    ix = get_or_create_index()
    with ix.searcher() as searcher:
        parser = MultifieldParser(["title", "ingredients", "tags"], ix.schema)
        query = parser.parse(query)
        results = searcher.search(query, limit=None)  # Obtener todos los resultados primero
        
        # Calcular paginación
        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        paginated_results = results[start_index:end_index]
        
        # Crear los resultados en formato deseado
        formatted_results = [
            {
                "id": r["id"],
                "title": r["title"],
                "author": r["author"],
                "category": r["category"],
                "time": r["time"],
                "difficulty": r["difficulty"],
                "image_url": r["image_url"]
            } for r in paginated_results
        ]
        
        # Datos de metadatos para la paginación
        total_results = len(results)
        total_pages = (total_results + page_size - 1) // page_size
        
        return {
            "results": formatted_results,
            "total_results": total_results,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
        }


def get_categories_from_index():
    """
    Extrae las categorías únicas del índice Whoosh.
    """
    ix = get_or_create_index()
    categories = set()
    with ix.searcher() as searcher:
        for doc in searcher.documents():  # Iterar sobre todos los documentos
            if "category" in doc and doc["category"]:
                categories.add(doc["category"])
    return sorted(categories)


def get_time_and_difficulty_from_index():
    """
    Extrae los valores únicos de tiempo y dificultad del índice Whoosh.
    """
    ix = get_or_create_index()
    times = set()
    difficulties = set()
    with ix.searcher() as searcher:
        for doc in searcher.documents():  # Iterar sobre todos los documentos
            if "time" in doc and doc["time"] and doc["time"].lower() != "n/a":
                times.add(doc["time"].lower())  # Normalizamos a minúsculas
            if "difficulty" in doc and doc["difficulty"] and doc["difficulty"].lower() != "n/a":
                difficulties.add(doc["difficulty"].lower())  # Normalizamos a minúsculas
    return sorted(times), sorted(difficulties)


def recommend_recipes(recipe_id, top_n=5):
    """
    Recomienda recetas similares basadas en el contenido, dando más peso a los ingredientes.
    
    :param recipe_id: ID de la receta objetivo.
    :param top_n: Número de recetas a recomendar.
    :return: Lista de recetas recomendadas.
    """
    ix = get_or_create_index()

    with ix.searcher() as searcher:
        # Obtener la receta objetivo
        target_recipe = searcher.document(id=recipe_id)
        if not target_recipe:
            return []

        # Crear una consulta con mayor peso para los ingredientes
        query = (
            f'title:"{target_recipe["title"]}"^1.0 OR '  # Peso normal para el título
            f'ingredients:({target_recipe["ingredients"]})^2.0 OR '  # Peso más alto para ingredientes
            f'category:"{target_recipe["category"]}"^1.0 OR '  # Peso normal para categoría
            f'time:"{target_recipe["time"]}"^0.5 OR '  # Menor peso para tiempo
            f'difficulty:"{target_recipe["difficulty"]}"^0.5 OR '  # Menor peso para dificultad
            f'tags:({target_recipe["tags"]})^1.0'  # Peso normal para tags
        )

        # Crear un parser con soporte para boosting
        parser = MultifieldParser(
            ["title", "ingredients", "category", "time", "difficulty", "tags"],
            schema=ix.schema,
            group=OrGroup
        )
        parsed_query = parser.parse(query)

        # Buscar recetas similares en el índice
        results = searcher.search(parsed_query, limit=top_n + 1)  # +1 para excluir la receta objetivo
        recommendations = []

        for result in results:
            if result["id"] != recipe_id:  # Excluir la receta objetivo
                recommendations.append({
                    "id": result["id"],
                    "title": result["title"],
                    "category": result["category"],
                    "time": result["time"],
                    "difficulty": result["difficulty"],
                    "image_url": result.get("image_url", "N/A"),
                    "score": result.score,  # Puntuación de similitud
                })

        return recommendations