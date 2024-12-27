import requests
from bs4 import BeautifulSoup
from apps.home.models import Receta, Autor, Categoria

# lineas para evitar error SSL
import os, ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

def scrape_recipes_by_category(categories):
    
    #borrar tablas
    Receta.objects.all().delete()
    Categoria.objects.all().delete()
    Autor.objects.all().delete()
    
    base_url = "https://canalcocina.es/recetas/?buscar-texto=&categoria="
    all_recipes = []

    for category_name in categories:
        url = f"{base_url}{category_name}"
        print(f"Procesando categoría: {category_name} - URL: {url}")
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Error al acceder a la categoría: {category_name}, Status Code: {response.status_code}")
            continue

        soup = BeautifulSoup(response.content, 'lxml')

        # Obtener o crear la categoría
        category, created = Categoria.objects.get_or_create(name=category_name)
        if created:
            print(f"Categoría creada: {category_name}")

        recipies = soup.find_all('a', class_='row box-details recipe')
        
        for recipe in recipies:
            title_tag = recipe.find('span', class_='title')
            title = title_tag.text.strip() if title_tag else "Título no encontrado"
            
            link = recipe['href'] if recipe.has_attr('href') else "#"
            full_link = f"https://canalcocina.es{link}"

            all_recipes.append({
                'title': title,
                'link': full_link,
                'category': category_name
            })

    print(f"Recetas encontradas: {len(all_recipes)}")
    return all_recipes


def scrape_recipe(url, category):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error al acceder a la receta: {url}, Status Code: {response.status_code}")
        return

    soup = BeautifulSoup(response.content, 'lxml')

    # Extraer título
    title = soup.find("h1", class_="underline", itemprop="name")
    if title:
        title = title.text.split('\n')[0].strip()
    else:
        print("No se pudo encontrar el título.")
        return

    # Extraer nombre del autor
    author_name = soup.find(itemprop="author")
    author_name = author_name.text.strip() if author_name else None

    # Extraer programa
    program = soup.find("a", title=True)
    program = program.text.strip() if program else None

    # Extraer tiempo, dificultad y comensales
    time_info = soup.find("h1", class_="underline").text if soup.find("h1", class_="underline") else ""
    time_parts = [part.strip() for part in time_info.split('|') if ':' in part]
    time = next((part.split(':')[1].strip() for part in time_parts if 'Tiempo' in part), None)
    difficulty = next((part.split(':')[1].strip() for part in time_parts if 'Dificultad' in part), None)
    servings = next((part.split(':')[1].strip() for part in time_parts if 'Comensales' in part), None)

    # Extraer imagen
    image_tag = soup.find(itemprop="image")
    image_url = image_tag['src'] if image_tag else None

    # Extraer ingredientes
    ingredients = [
        li.text.strip() for li in soup.find_all(itemprop="recipeIngredient")
    ]

    # Extraer instrucciones
    instructions_container = soup.find(itemprop="recipeInstructions")
    if instructions_container:
        instructions = "\n".join([
            p.text.strip() for p in instructions_container.find_all("p")
        ])
    else:
        instructions = ""

    # Extraer tags
    tags_container = soup.select(".list-grey a")
    tags = ", ".join([a.text.strip() for a in tags_container])

    # Crear o buscar al autor
    author = None
    if author_name:
        author, created = Autor.objects.get_or_create(name=author_name)
        if created:
            print(f"Nuevo autor creado: {author_name}")

    # Crear o actualizar la receta
    Receta.objects.update_or_create(
        source_url=url,
        defaults={
            "title": title,
            "author": author,  # Asociar el autor
            "category": category,  # Asociar la categoría
            "program": program,
            "time": time,
            "difficulty": difficulty,
            "servings": servings,
            "ingredients": "\n".join(ingredients),
            "instructions": instructions,
            "tags": tags,
            "image_url": image_url,
        }
    )

    print(f"Receta guardada/actualizada: {title}")


def scrape_and_save_by_category(categories):
    print("Inicio del proceso general de scraping y guardado.")
    recipes = scrape_recipes_by_category(categories)
    for recipe_data in recipes:
        # Procesar cada receta
        scrape_recipe(recipe_data['link'], recipe_data['category'])
    print("Proceso completado.")


