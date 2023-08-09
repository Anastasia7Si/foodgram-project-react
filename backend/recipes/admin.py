from django.contrib import admin
from django.contrib.admin import display
from users.models import Following

from .models import (Favorite, Ingredient, IngredientAmount, Recipe,
                     ShoppingCart, Tag)


class IngredientInline(admin.TabularInline):
    model = IngredientAmount
    min_num = 1


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    fields = [('name', 'measurement_unit')]
    list_filter = ('name',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (IngredientInline,)
    list_display = ('name', 'author', 'is_favorited_count')
    list_filter = ('name', 'author', 'tags')

    @display(description='Количество в избранных')
    def is_favorited_count(self, obj):
        return obj.favorites.count()


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    list_filter = ('name', 'slug')


@admin.register(IngredientAmount)
class IngredientAmountAdmin(admin.ModelAdmin):
    description = 'Ингредиенты в рецептах'
    list_display = ('ingredient', 'recipe', 'amount')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    list_filter = ('user',)


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    list_filter = ('user',)


@admin.register(Following)
class FollowingAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')
    list_filter = ('user',)
