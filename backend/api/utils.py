from django.db.models import Sum
from django.http import HttpResponse
from recipes.models import IngredientAmount
from rest_framework import status
from rest_framework.response import Response


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
    for number, item in enumerate(ingredients_cart):
        shopping_list += (
            f'\n- {item["ingredient__name"]} '
            f'({item["ingredient__measurement_unit"]})'
            f' - {item["amount"]}'
        )
        if number < ingredients_cart.count() - 1:
            shopping_list += ', '
    shopping_list += '\n\nFoodgram'
    filename = 'shopping_list.pdf'
    response = HttpResponse(shopping_list, 'Content-Type: application/pdf')
    response['Content-Disposition'] = f'attachment; filename={filename}'
    return response
