from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Nombre único del autor
    bio = models.TextField(blank=True, null=True)  # Biografía del autor

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Nombre único de la categoría

    def __str__(self):
        return self.name

class Recipe(models.Model):
    title = models.CharField(max_length=255)  # Título de la receta
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, blank=True, null=True, related_name="recipes") 
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, related_name="recipes")
    program = models.CharField(max_length=255, blank=True, null=True)  # Programa asociado
    time = models.CharField(max_length=100, blank=True, null=True)  # Etiqueta de tiempo
    difficulty = models.CharField(max_length=50, blank=True, null=True)  # Dificultad
    servings = models.CharField(max_length=50, blank=True, null=True)  # Número de comensales
    ingredients = models.TextField()  # Lista de ingredientes
    steps = models.TextField()  # Pasos de preparación
    tags = models.TextField(blank=True, null=True)  # Tags o categorías asociadas

    def __str__(self):
        return self.title
    

from django.contrib.auth.models import User
from django.db import models

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe_id = models.CharField(max_length=255)  # ID único de la receta en Whoosh
    recipe_title = models.CharField(max_length=255)  # Título de la receta para mostrar en favoritos
    recipe_image = models.CharField(max_length=255, blank=True, null=True)  # URL de la imagen

    class Meta:
        unique_together = ('user', 'recipe_id')  # Evitar duplicados

    def __str__(self):
        return f"{self.user.username} - {self.recipe_title}"

