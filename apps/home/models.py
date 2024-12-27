from django.db import models

class Receta(models.Model):
    title = models.CharField(max_length=255)  # Título de la receta
    author = models.CharField(max_length=100, blank=True, null=True)  # Autor de la receta
    program = models.CharField(max_length=255, blank=True, null=True)  # Programa asociado
    time = models.CharField(max_length=100, blank=True, null=True)  # Tiempo total
    difficulty = models.CharField(max_length=50, blank=True, null=True)  # Dificultad
    servings = models.CharField(max_length=50, blank=True, null=True)  # Número de comensales
    ingredients = models.TextField()  # Lista de ingredientes
    instructions = models.TextField()  # Pasos de preparación
    image_url = models.URLField(blank=True, null=True)  # URL de la imagen principal
    tags = models.TextField(blank=True, null=True)  # Tags o categorías asociadas
    source_url = models.URLField()  # Enlace a la receta original

    def __str__(self):
        return self.title
