from django.db import models

class Autor(models.Model):
    nombre = models.CharField(max_length=100, unique=True)  # Nombre único del autor
    bio = models.TextField(blank=True, null=True)  # Biografía del autor

    def __str__(self):
        return self.name

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)  # Nombre único de la categoría

    def __str__(self):
        return self.name

class Receta(models.Model):
    title = models.CharField(max_length=255)  # Título de la receta
    autor = models.ForeignKey(Autor, on_delete=models.SET_NULL, blank=True, null=True, related_name="recipes")  # Relación con el autor
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, blank=True, null=True, related_name="recipes")  # Relación con la categoría
    programa = models.CharField(max_length=255, blank=True, null=True)  # Programa asociado
    tiempo = models.CharField(max_length=100, blank=True, null=True)  # Tiempo total
    dificultad = models.CharField(max_length=50, blank=True, null=True)  # Dificultad
    comensales = models.CharField(max_length=50, blank=True, null=True)  # Número de comensales
    ingredientes = models.TextField()  # Lista de ingredientes
    instrucciones = models.TextField()  # Pasos de preparación
    etiquetas = models.TextField(blank=True, null=True)  # Tags o categorías asociadas

    def __str__(self):
        return self.title
