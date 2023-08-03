from django.db.models import F
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField, IntegerField
from rest_framework.relations import PrimaryKeyRelatedField

from recipes.models import Recipe, Tag, Ingredient, IngredientQuantity
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


class QuantityWriteSerializer(serializers.ModelSerializer):
    """Сериализатор записи количества ингредиента."""
    id = IntegerField(write_only=True)

    class Meta:
        model = IngredientQuantity
        fields = ('id', 'quantity')


class RecipeReadSerializer(serializers.ModelSerializer):
    """Сериализатор просмотра рецепта."""
    tags = TagSerializer(many=True)
    author = UserReadSerializer()
    ingredients = SerializerMethodField()
    image = Base64ImageField()
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()

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

    def get_ingredients(self, obj):
        recipe = obj
        ingredients = recipe.ingredients.values(
            'id',
            'name',
            'measurement_unit',
            quantity=F('ingredientquantity__quantity')
        )
        return ingredients

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


class RecipeReWriteSerializer(serializers.ModelSerializer):
    """Сериализатор создания рецепта."""
    tags = PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)
    author = UserReadSerializer(read_only=True)
    ingredients = QuantityWriteSerializer(many=True)
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

    def validate_ingredients(self, value):
        ingredients = value
        if not ingredients:
            return ('Необходимо добавить хотя бы один ингредиент!')
        ingredients_list = []
        for item in ingredients:
            ingredient = get_object_or_404(Ingredient, id=item['id'])
            if ingredient in ingredients_list:
                return ('Ингредиент повторяется в рецепте!')
            if int(item['quantity']) <= 0:
                return ('Нулевое количество ингредиента!')
            ingredients_list.append(ingredient)
        return value

    def validate_tags(self, value):
        tags = value
        if not tags:
            return ('Необходимо добавить хотя бы один тэг!')
        tags_list = []
        for tag in tags:
            if tag in tags_list:
                return ('Необходимо ввести уникальные тэги!')
            tags_list.append(tag)
        return value

    def create_ingredients_quantity(self, recipe, ingredients):
        IngredientQuantity.objects.bulk_create(
            [IngredientQuantity(
                ingredient=Ingredient.objects.get(id=ingredient['id']),
                recipe=recipe,
                quantity=ingredient['quantity']
            ) for ingredient in ingredients]
        )

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.create_ingredients_quantity(recipe=recipe,
                                         ingredients=ingredients)
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredient')
        instance = super().update(instance, validated_data)
        instance.tags.clear()
        instance.tags.set(tags)
        instance.ingredients.clear()
        self.create_ingredients_quantity(recipe=instance,
                                         ingredients=ingredients)
        instance.save()
        return instance

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeReadSerializer(instance, context=context).data
