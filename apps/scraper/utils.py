import requests
from bs4 import BeautifulSoup
from apps.home.models import Recipe, Category, Author

# Líneas para evitar error SSL
import os
import ssl

if not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
    ssl._create_default_https_context = ssl._create_unverified_context

BASE_URL = "https://canalcocina.es/recetas/?buscar-texto=&categoria="
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def scrape_recipes_by_category(categories):
    # Borrar tablas
    Recipe.objects.all().delete()
    Category.objects.all().delete()
    Author.objects.all().delete()

    all_recipes = []

    for category_name in categories:
        url = f"{BASE_URL}{category_name}"
        print(f"Procesando categoría: {category_name} - URL: {url}")
        try:
            response = requests.get(url, headers=HEADERS)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Error al acceder a la categoría {category_name}: {e}")
            continue

        soup = BeautifulSoup(response.content, 'lxml')

        # Obtener o crear la categoría
        category, created = Category.objects.get_or_create(name=category_name)
        if created:
            print(f"Categoría creada: {category_name}")

        recipes = soup.find_all('a', class_='row box-details recipe')

        for recipe in recipes:
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


def scrape_recipe(url, category_name):
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error al acceder a la receta {url}: {e}")
        return

    soup = BeautifulSoup(response.content, 'lxml')

    # Extraer título
    title_tag = soup.find("h1", class_="underline", itemprop="name")
    title = title_tag.contents[0].strip() if title_tag else None
    if not title:
        print(f"\tNo se encontró un título para la receta en {url}.")
        return

    # Extraer nombre del autor
    author_tag = soup.find(itemprop="author")
    author_name = author_tag.text.strip() if author_tag else None

    # Extraer programa
    program_tag = soup.find("a", title=True)
    program = program_tag.text.replace('PROGRAMA:', '').strip() if program_tag else None

    # Extraer tiempo, dificultad y comensales
    details_tag = title_tag.find_all("span", style="font-size:14px;")
    time, difficulty, servings = None, None, None

    for detail in details_tag:
        text = detail.text.strip()
    
        # Separar las partes usando "|"
        parts = text.split("|")
    
        for part in parts:
            if "Tiempo:" in part:
                time = part.split(":")[1].strip()
            elif "Dificultad:" in part:
                difficulty = part.split(":")[1].strip()
            elif "Comensales:" in part:
                servings = part.split(":")[1].strip()

    # Extraer ingredientes
    ingredients = [li.text.strip() for li in soup.find_all(itemprop="recipeIngredient")]
    if not ingredients:
        print(f"\tNo se encontraron ingredientes para la receta: {title}.")
        return

    # Extraer instrucciones
    instructions_container = soup.find(itemprop="recipeInstructions")
    instructions = "\n".join([p.text.strip() for p in instructions_container.find_all("p")]) if instructions_container else ""

    # Extraer tags
    tags_container = soup.select(".list-grey a")
    tags = ", ".join([a.text.strip() for a in tags_container])

    # Crear o buscar al autor
    author = None
    if author_name:
        author, created = Author.objects.get_or_create(name=author_name)
        if created:
            print(f"\tNuevo autor creado: {author_name}")

    # Crear o buscar la categoría
    category, created = Category.objects.get_or_create(name=category_name)
    if created:
        print(f"\tNueva categoría creada: {category_name}")

    # Crear o actualizar la receta
    recipe, created = Recipe.objects.update_or_create(
        title=title,
        defaults={
            "author": author,
            "category": category,
            "program": program,
            "time": time,
            "difficulty": difficulty,
            "servings": servings,
            "ingredients": "\n".join(ingredients),
            "steps": instructions,
            "tags": tags,
        }
    )

    action = "creada" if created else "actualizada"
    print(f"Receta {action}: {title}")


def scrape_and_save_by_category(categories):
    print("Inicio del proceso general de scraping y guardado.")
    recipes = scrape_recipes_by_category(categories)
    for recipe_data in recipes:
        scrape_recipe(recipe_data['link'], recipe_data['category'])
    print("Proceso completado.")
