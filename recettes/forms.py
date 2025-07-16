
from django import forms
from .models import Recipe, Comment, Reservation

class ReservationForm(forms.ModelForm):
    confirm = forms.BooleanField(
        label="En cochant cette case, vous reconnaissez que les données saisies sont correctes.",
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    class Meta:
        model = Reservation
        fields = ['name', 'age', 'phone', 'email', 'hour', 'location']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Âge'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Téléphone'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'hour': forms.Select(attrs={'class': 'form-select'}),
            'location': forms.Select(attrs={'class': 'form-select'}),
        }

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ["title", "description", "ingredients", "instructions", "image"]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "style": "border:2px solid #ff8700; border-radius:8px; background:#181818; color:#ff8700 !important; font-size:1.1em;",
                "placeholder": "Titre de la recette"
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "style": "border:2px solid #ff8700; border-radius:8px; background:#181818; color:#ff8700 !important; font-size:1.1em; min-height:90px;",
                "placeholder": "Description"
            }),
            "ingredients": forms.Textarea(attrs={
                "class": "form-control",
                "style": "border:2px solid #ff8700; border-radius:8px; background:#181818; color:#ff8700 !important; font-size:1.1em; min-height:90px;",
                "placeholder": "Ingrédients"
            }),
            "instructions": forms.Textarea(attrs={
                "class": "form-control",
                "style": "border:2px solid #ff8700; border-radius:8px; background:#181818; color:#ff8700 !important; font-size:1.1em; min-height:90px;",
                "placeholder": "Instructions"
            }),
            "image": forms.ClearableFileInput(attrs={
                "class": "form-control",
                "style": "color:#ff8700 !important; background:#232323; border:none;"
            }),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]