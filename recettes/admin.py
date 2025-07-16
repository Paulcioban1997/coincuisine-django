from django.contrib import admin
from .models import Recipe, Comment
from django.utils.html import format_html 



class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'image_tag')

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="60" height="60"/>', obj.image.url)
        return "Aucune image"
    image_tag.short_description = 'Image'

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Comment)
