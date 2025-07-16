from django.urls import path
from .views import RecipeListView, RecipeDetailView, RecipeCreateView, RecipeUpdateView, RecipeDeleteView, AjouterRecetteView, UserLogoutView, AddCommentAjaxView, ReservationView
from .views_signup import SignUpView

urlpatterns = [
    path("", RecipeListView.as_view(), name="recipe_list"),
    path("ajouter/", AjouterRecetteView.as_view(), name="ajouter_recette"),
    path("<int:pk>/", RecipeDetailView.as_view(), name="recipe_detail"),
    path("new/", RecipeCreateView.as_view(), name="recipe_create"),
    path("<int:pk>/edit/", RecipeUpdateView.as_view(), name="recipe_update"),
    path("<int:pk>/delete/", RecipeDeleteView.as_view(), name="recipe_delete"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("<int:pk>/add_comment/", AddCommentAjaxView.as_view(), name="add_comment_ajax"),
    path("reservation/", ReservationView.as_view(), name="reservation"),
]
