from django.db.models import Sum
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response

from recipes.models import IngredientAmount


def download_shopping_cart(request):
    user = request.user
    if not user.shopping_cart.exists():
        return Response({'errors': 'Список покупок пуст!'},
                        status=status.HTTP_400_BAD_REQUEST)
    shopping_list = (
        f'Список покупок: {user.get_full_name()}\n\n'
    )
    ingredients_cart = IngredientAmount.objects.filter(
        recipe__shopping_cart__user=user
    ).values(
        'ingredient__name',
        'ingredient__measurement_unit'
    ).annotate(amount=Sum('amount')
               ).order_by()
    for item in ingredients_cart:
        shopping_list += (
            f'\n- {item["ingredient__name"]} '
            f'({item["ingredient__measurement_unit"]})'
            f' - {item["amount"]}'
        )
    shopping_list += '\n\nFoodgram'
    filename = 'shopping_list.txt'
    response = HttpResponse(shopping_list, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename={filename}'
    return response
