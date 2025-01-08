import hashlib
import requests
from bs4 import BeautifulSoup
from apps.scraper.whoosh_index import get_or_create_index
import os
import ssl

# Líneas para evitar error SSL
if not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
    ssl._create_default_https_context = ssl._create_unverified_context

BASE_URL = "https://canalcocina.es/recetas/?buscar-texto=&categoria="
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def scrape_recipes_by_category(categories):
    ix = get_or_create_index()
    writer = ix.writer()
    recipe_count = 0  # Contador de recetas

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
        recipes = soup.find_all('a', class_='row box-details recipe')

        for recipe in recipes:
            title_tag = recipe.find('span', class_='title')
            title = title_tag.text.strip() if title_tag else "Título no encontrado"
            link = recipe['href'] if recipe.has_attr('href') else "#"
            full_link = f"https://canalcocina.es{link}"

            if scrape_and_index_recipe(full_link, category_name, writer):
                recipe_count += 1  # Incrementar el contador

    writer.commit()
    print(f"Recetas encontradas: {recipe_count}")
    return recipe_count

def scrape_and_index_recipe(url, category_name, writer):
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error al acceder a la receta {url}: {e}")
        return False

    soup = BeautifulSoup(response.content, 'lxml')
    title_tag = soup.find("h1", class_="underline", itemprop="name")
    title = title_tag.contents[0].strip() if title_tag else None

    if not title:
        print(f"\tNo se encontró un título para la receta en {url}.")
        return False

    author_tag = soup.find(itemprop="author")
    author_name = author_tag.text.strip() if author_tag else "Desconocido"

    program_tag = soup.find("a", title=True)
    program = program_tag.text.replace('PROGRAMA:', '').strip() if program_tag else "N/A"

    details_tag = title_tag.find_all("span", style="font-size:14px;")
    time, difficulty, servings = None, None, None
    for detail in details_tag:
        text = detail.text.strip()
        parts = text.split("|")
        for part in parts:
            if "Tiempo:" in part:
                time = part.split(":")[1].strip()
            elif "Dificultad:" in part:
                difficulty = part.split(":")[1].strip()
            elif "Comensales:" in part:
                servings = part.split(":")[1].strip()

    ingredients = [li.text.strip() for li in soup.find_all(itemprop="recipeIngredient")]
    if not ingredients:
        print(f"\tNo se encontraron ingredientes para la receta: {title}.")
        return False

    instructions_container = soup.find(itemprop="recipeInstructions")
    instructions = "\n".join([p.text.strip() for p in instructions_container.find_all("p")]) if instructions_container else ""

    tags_container = soup.select(".list-grey a")
    tags = ", ".join([a.text.strip() for a in tags_container])
    
    # Extraer la URL de la imagen
    image_container = soup.find("div", class_="bigger")
    image_tag = image_container.find("img") if image_container else None
    image_url = image_tag["src"] if image_tag and "src" in image_tag.attrs else "N/A"
    
    formatted_category_name = category_name.replace("-", " ").title()

    # Generar un ID único basado en la URL
    recipe_id = hashlib.md5(url.encode('utf-8')).hexdigest()

    writer.add_document(
        id=url,
        title=title,
        author=author_name,
        category=formatted_category_name,
        program=program,
        time=time or "N/A",
        difficulty=difficulty or "N/A",
        servings=servings or "N/A",
        ingredients="\n".join(ingredients),
        steps=instructions,
        tags=tags,
        image_url=image_url
    )
    print(f"Receta indexada: {title}")
    return True

def scrape_and_save_by_category(categories):
    print("Inicio del proceso general de scraping.")
    recipes = scrape_recipes_by_category(categories)
    print(f"Total de recetas indexadas: {recipes}")
    print("Proceso completado.")
    return recipes
