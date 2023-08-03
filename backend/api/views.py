from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response

from .filters import IngredientFilter, RecipeFilter
from .serializers import (TagSerializer, IngredientSerializer,
                          RecipeReadSerializer, RecipeReWriteSerializer)
from .permissions import IsAuthorOrReadOnly, IsAdminOrReadOnly
from .pagination import Pagination
from .utils import download_shopping_cart_file
from recipes.models import (Recipe, Tag, Ingredient,
                            Favorite, Shopping_cart)
from users.serializers import RecipeShorPresentationtSerializer


class IngredientViewSet(ReadOnlyModelViewSet):
    """Вьюсет ингредиентов."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter


class TagViewSet(ReadOnlyModelViewSet):
    """Вьюсет тэгов."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)


class RecipeViewSet(ModelViewSet):
    """Вьюсет рецептов."""
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrReadOnly | IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = Pagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeReWriteSerializer

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk):
        if request.method == 'POST':
            return self.add_to(Favorite, request.user, pk)
        return self.delete_from(Favorite, request.user, pk)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk):
        if request.method == 'POST':
            return self.add_to(Shopping_cart, request.user, pk)
        return self.delete_from(Shopping_cart, request.user, pk)

    def add_to(self, model, user, pk):
        if model.objects.filter(user=user, recipe__id=pk).exists():
            return Response({'errors': 'Данный рецепт уже добавлен!'},
                            status=status.HTTP_400_BAD_REQUEST)
        model.objects.create(user=user,
                             recipe=get_object_or_404(Recipe, id=pk))
        serializer = RecipeShorPresentationtSerializer(
            get_object_or_404(Recipe, id=pk))
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_from(self, model, user, pk):
        if model.objects.filter(user=user, recipe__id=pk).exists():
            model.objects.filter(user=user, recipe__id=pk).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'errors': 'Данный рецепт уже удален!'},
                        status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        if request.method == 'GET':
            return download_shopping_cart_file(request)
        return Response(status=status.HTTP_400_BAD_REQUEST)
