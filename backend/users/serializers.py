from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer, UserCreateSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from recipes.models import Recipe
from .models import Following

User = get_user_model()


class UserCreateSerializer(UserCreateSerializer):
    """Сериализатор создания пользователя."""
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name',
                  'last_name', 'password')


class UserReadSerializer(UserSerializer):
    """Сериализатор просмотра профиля пользователя."""
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email',
                  'first_name', 'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        if self.context.get('request').user.is_anonymous:
            return False
        return Following.objects.filter(
            user=self.context.get('request').user, author=obj
        ).exists()


class FollowingRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор рецептов из подписок."""
    class Meta:
        model = Recipe
        fields = ('name', 'image', 'cooking_time')


class RecipeShorPresentationtSerializer(serializers.ModelSerializer):
    """Сериализатор превью рецепта."""
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class FollowingSerializer(UserReadSerializer):
    """Сериализатор подписок."""
    recipes_count = serializers.IntegerField(
        source='recipes_set.count',
        read_only=True)
    recipes = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = UserReadSerializer.Meta.fields + (
            'recipes_count', 'recipes'
        )
        read_only_fields = ('username', 'email', 'first_name',
                            'last_name')

    def validate(self, data):
        if self.context.get('request').user == self.context.get('author_id'):
            return serializers.ValidationError({
                'errors': 'Нельзя подписаться на собственный профиль!'})
        if Following.objects.filter(
            user=self.context.get('request').user,
            author=self.context.get('author_id')
        ).exists():
            return serializers.ValidationError({
                'errors': 'Вы уже подписанны на этого автора!'})
        return data

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        recipes = obj.recipes.all()
        if limit:
            recipes = recipes[:int(limit)]
        serializer = RecipeShorPresentationtSerializer(
            recipes, many=True, read_only=True)
        return serializer.data
