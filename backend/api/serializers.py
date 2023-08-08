from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from recipes.models import Recipe, Tag, Ingredient, IngredientAmount
from users.serializers import UserReadSerializer

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор тэгов."""
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов."""
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class AmountRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов в рецепте."""
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientAmount
        fields = ('id', 'name', 'measurement_unit', 'amount')


class AddIngredienIntRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления ингредиентов в рецепт."""
    id = serializers.IntegerField(write_only=True)
    amount = serializers.IntegerField(write_only=True)

    class Meta:
        model = IngredientAmount
        fields = ('id', 'amount')


class RecipeReadSerializer(serializers.ModelSerializer):
    """Сериализатор просмотра рецепта."""
    tags = TagSerializer(many=True)
    author = UserReadSerializer()
    ingredients = AmountRecipeSerializer(
        read_only=True,
        many=True,
        source='ingredientsamount'
    )
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )
        read_only_fields = ('tags', 'author', 'is_favorited',
                            'is_in_shopping_cart')

    def get_is_favorited(self, obj):
        if self.context.get('request').user.is_anonymous:
            return False
        return self.context.get('request').user.favorites.filter(
            recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        if self.context.get('request').user.is_anonymous:
            return False
        return self.context.get('request').user.shopping_cart.filter(
            recipe=obj).exists()


class RecipeWriteSerializer(serializers.ModelSerializer):
    """Сериализатор создания рецепта."""
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True)
    author = UserReadSerializer(read_only=True)
    ingredients = AddIngredienIntRecipeSerializer(many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def validate_ingredients(self, ingredients):
        if not ingredients:
            return ('Необходимо добавить хотя бы один ингредиент!')
        for item in ingredients:
            if item['amount'] <= 0:
                return ('Нулевое количество ингредиента!')
        ingredients_list = [ingredient['id'] for ingredient in ingredients]
        if len(ingredients_list) != len(set(ingredients_list)):
            return ('Ингредиент повторяется в рецепте!')
        return ingredients

    def validate_tags(self, tags):
        if not tags:
            return ('Необходимо добавить хотя бы один тэг!')
        if len(tags) != len(set(tags)):
            return ('Необходимо ввести уникальные тэги!')
        return tags

    def add_ingredients(self, ingredients, recipe):
        ingredients_list = []
        for ingredient in ingredients:
            new_ingredient = IngredientAmount(
                ingredient=get_object_or_404(Ingredient, id=ingredient['id']),
                recipe=recipe,
                amount=ingredient['amount']
            )
            ingredients_list.append(new_ingredient)
        IngredientAmount.objects.bulk_create(ingredients_list)
        return recipe

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.add_ingredients(recipe=recipe,
                             ingredients=ingredients)
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients', None)
        if tags is not None:
            instance.tags.set(tags)
        if ingredients is not None:
            instance.ingredients.clear()
        self.add_ingredients(recipe=instance,
                             ingredients=ingredients)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        return RecipeReadSerializer(instance, context=self.context).data
