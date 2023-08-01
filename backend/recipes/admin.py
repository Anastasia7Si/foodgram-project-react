from django.contrib import admin
from django.contrib.admin import display

from .models import (Ingredient, Recipe, Tag,
                     IngredientQuantity, Favorite, Shopping_cart)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    fields = [('name', 'measurement_unit')]
    list_filter = ('name',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'is_favorited_count')
    list_filter = ('name', 'author', 'tags')

    @display(description='Количество в избранных')
    def is_favorited_count(self, obj):
        return obj.favorites.count()


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    list_filter = ('name', 'slug')


@admin.register(IngredientQuantity)
class IngredientQuantityAdmin(admin.ModelAdmin):
    description = 'Ингредиенты в рецептах'
    list_display = ('ingredient', 'recipe', 'quantity')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


@admin.register(Shopping_cart)
class Shopping_cartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
