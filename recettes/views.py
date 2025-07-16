from django.shortcuts import redirect

from django.contrib.auth.views import LoginView

class UserLoginView(LoginView):
    template_name = 'registration/login.html'
from .forms import ReservationForm
from django.shortcuts import render, redirect

# Vue pour la réservation
from django.views.generic import View
class ReservationView(View):
    def get(self, request):
        form = ReservationForm()
        return render(request, 'recipes/recettes/reservation.html', {'form': form})

    def post(self, request):
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'recipes/recettes/reservation.html', {'form': ReservationForm(), 'success': True})
        return render(request, 'recipes/recettes/reservation.html', {'form': form})

from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from .models import Recipe, Comment
from .forms import RecipeForm, CommentForm
from django.shortcuts import redirect

# AJAX endpoint for adding a comment to a recipe
@method_decorator(csrf_exempt, name='dispatch')
class AddCommentAjaxView(LoginRequiredMixin, View):
    def post(self, request, pk):
        try:
            data = json.loads(request.body)
            content = data.get('content', '').strip()
            if not content:
                return JsonResponse({'success': False, 'error': 'Empty comment'}, status=400)
            recipe = Recipe.objects.get(pk=pk)
            comment = Comment.objects.create(recipe=recipe, author=request.user, content=content)
            return JsonResponse({'success': True, 'author': request.user.username, 'content': comment.content})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

class UserLoginView(LoginView):
    template_name = 'registration/login.html'

class UserLogoutView(LogoutView):
    next_page = '/accounts/login/'


class RecipeListView(ListView):
    model = Recipe
    template_name = "recipes/recettes/liste_recettes.html"
    context_object_name = "recettes"

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q', '').strip()
        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) | Q(description__icontains=q)
            )
        return queryset

from django.db.models import Q

class RecipeDetailView(DetailView):
    model = Recipe
    template_name = "recipes/recipe_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        recipe = self.get_object()
        if "rating" in request.POST and request.user.is_authenticated:
            try:
                rating = int(request.POST.get("rating"))
                if 1 <= rating <= 5:
                    recipe.rating = rating
                    recipe.save()
            except Exception:
                pass
        elif request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.recipe = recipe
                comment.author = request.user
                comment.save()
        return redirect("recipe_detail", pk=recipe.pk)

class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = "recipes/recipe_form.html"
    success_url = reverse_lazy("recipe_list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class RecipeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = "recipes/recipe_form.html"
    success_url = reverse_lazy("recipe_list")

    def test_func(self):
        return self.get_object().author == self.request.user

class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Recipe
    template_name = "recipes/recipe_confirm_delete.html"
    success_url = reverse_lazy("recipe_list")

    def test_func(self):
        return self.get_object().author == self.request.user

class AjouterRecetteView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/ajouter_recette.html'
    success_url = reverse_lazy('recipe_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_authenticated


