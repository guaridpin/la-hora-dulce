from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID
import os

def create_index():
    if not os.path.exists("index"):
        os.mkdir("index")
    schema = Schema(title=TEXT(stored=True), link=ID(stored=True), image=ID(stored=True))
    ix = create_in("index", schema)
    return ix

from whoosh.index import open_dir
from whoosh.qparser import QueryParser

def index_recipes():
    ix = create_index()
    writer = ix.writer()
    recipes = Recipe.objects.all()
    for recipe in recipes:
        writer.add_document(title=recipe.title, link=recipe.link, image=recipe.image)
    writer.commit()

def search_recipes(query):
    ix = open_dir("index")
    with ix.searcher() as searcher:
        query_parser = QueryParser("title", ix.schema)
        query_obj = query_parser.parse(query)
        results = searcher.search(query_obj)
        return [(r['title'], r['link'], r['image']) for r in results]
