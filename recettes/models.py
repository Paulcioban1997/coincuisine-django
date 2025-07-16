
from django.db import models
from django.contrib.auth.models import User

class Reservation(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    hour = models.CharField(max_length=5, choices=[(f"{h:02d}:00", f"{h:02d}:00") for h in range(14, 23)])
    location = models.CharField(max_length=20, choices=[('terrasse', 'Terrasse'), ('interieur', "À l'intérieur")])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.email})"


class Recipe(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    ingredients = models.TextField()    # ← Ajouté
    instructions = models.TextField()   # ← Ajouté
    image = models.ImageField(upload_to='recettes/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(default=0)  # 0-5 stars

    def __str__(self):
        return self.title

class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author} - {self.recipe.title}"

