from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Recipe, Comment
from .forms import RecipeForm, CommentForm

class RecipeModelTest(TestCase):
    def test_str(self):
        user = User.objects.create_user(username="testuser")
        recipe = Recipe.objects.create(title="Test", author=user, description="desc", ingredients="ing", instructions="inst")
        self.assertEqual(str(recipe), "Test")

class CommentModelTest(TestCase):
    def test_str(self):
        user = User.objects.create_user(username="testuser")
        recipe = Recipe.objects.create(title="Test", author=user, description="desc", ingredients="ing", instructions="inst")
        comment = Comment.objects.create(recipe=recipe, author=user, content="Nice!",)
        self.assertIn("testuser", str(comment))
        self.assertIn("Test", str(comment))


class RecipeDetailViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser")
        self.recipe = Recipe.objects.create(title="Test", author=self.user, description="desc", ingredients="ing", instructions="inst")


class RecipeCreateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="pass")

    def test_create_requires_login(self):
        response = self.client.get(reverse("ajouter_recette"))
        self.assertNotEqual(response.status_code, 200)  # Should redirect


class RecipeUpdateDeleteViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="pass")
        self.recipe = Recipe.objects.create(title="Test", author=self.user, description="desc", ingredients="ing", instructions="inst")

    def test_update_requires_login(self):
        response = self.client.get(reverse("recipe_update", args=[self.recipe.pk]))
        self.assertNotEqual(response.status_code, 200)

    def test_delete_requires_login(self):
        response = self.client.get(reverse("recipe_delete", args=[self.recipe.pk]))
        self.assertNotEqual(response.status_code, 200)

    def test_update_by_owner(self):
        self.client.login(username="testuser", password="pass")
        response = self.client.post(reverse("recipe_update", args=[self.recipe.pk]), {
            "title": "Updated",
            "description": "desc",
            "ingredients": "ing",
            "instructions": "inst",
        })
        self.recipe.refresh_from_db()
        self.assertEqual(self.recipe.title, "Updated")

    def test_delete_by_owner(self):
        self.client.login(username="testuser", password="pass")
        response = self.client.post(reverse("recipe_delete", args=[self.recipe.pk]))
        self.assertFalse(Recipe.objects.filter(pk=self.recipe.pk).exists())

class RecipeFormTest(TestCase):
    def test_valid_form(self):
        user = User.objects.create_user(username="testuser")
        form = RecipeForm(data={
            "title": "Test",
            "description": "desc",
            "ingredients": "ing",
            "instructions": "inst",
        })
        self.assertTrue(form.is_valid())

class CommentFormTest(TestCase):
    def test_valid_form(self):
        user = User.objects.create_user(username="testuser")
        recipe = Recipe.objects.create(title="Test", author=user, description="desc", ingredients="ing", instructions="inst")
        form = CommentForm(data={
            "author": user.pk,
            "content": "Nice!"
        })
        self.assertTrue(form.is_valid())
