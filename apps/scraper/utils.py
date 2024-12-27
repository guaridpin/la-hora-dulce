import requests
from bs4 import BeautifulSoup
from apps.home.models import Receta

def scrape_recipes_by_category(categories):
    base_url = "https://canalcocina.es/recetas/?buscar-texto=&categoria="
    all_recipes = []

    for category in categories:
        url = f"{base_url}{category}"
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Error al acceder a la categoría: {category}")
            continue

        soup = BeautifulSoup(response.content, 'html.parser')
        recipes = []

        for recipe_card in soup.select('.recipe-card'):
            title = recipe_card.select_one('.title').text.strip()
            link = recipe_card.select_one('a')['href']
            image = recipe_card.select_one('img')['src']
            recipes.append({
                'title': title,
                'link': link,
                'image': image,
                'category': category
            })

        all_recipes.extend(recipes)

    return all_recipes


def scrape_recipe(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extraer datos
    title = soup.find(itemprop="name").text.strip()
    author = soup.find(itemprop="author").text.strip() if soup.find(itemprop="author") else None
    program = soup.find("a", {"title": True}).text.strip() if soup.find("a", {"title": True}) else None
    time_info = soup.find("h1", class_="underline").text
    image_url = soup.find(itemprop="image")['src']
    ingredients = [li.text.strip() for li in soup.find_all(itemprop="recipeIngredient")]
    instructions = "\n".join([p.text.strip() for p in soup.find(itemprop="recipeInstructions").find_all("p")])
    tags = ", ".join([a.text.strip() for a in soup.select(".list-grey a")])
    
    # Crear o actualizar el modelo
    Receta.objects.update_or_create(
        source_url=url,
        defaults={
            "title": title,
            "author": author,
            "program": program,
            "time": "Extraer manualmente del texto en time_info",
            "difficulty": "Extraer manualmente del texto en time_info",
            "servings": "Extraer manualmente del texto en time_info",
            "ingredients": "\n".join(ingredients),
            "instructions": instructions,
            "image_url": image_url,
            "tags": tags,
        }
    )

def scrape_and_save_by_category(categories):
    recipes = scrape_recipes_by_category(categories)
    for recipe in recipes:
        Receta.objects.update_or_create(
            title=recipe['title'],
            defaults={
                'link': recipe['link'],
                'image': recipe['image'],
                'category': recipe['category']
            }
        )

