from django.db.models import Sum
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response

from recipes.models import IngredientQuantity


def download_shopping_cart_file(request):
    user = request.user
    if not user.shopping_cart.exists():
        return Response({'errors': 'Список покупок пуст!'},
                        status=status.HTTP_400_BAD_REQUEST)
    purchases = (
        f'Список покупок: {user.get_full_name()}\n\n'
    )
    purchases_cart = IngredientQuantity.objects.filter(
        recipe__shopping_cart__user=user
    ).values(
        'ingredient__name',
        'ingredient__measurement_unit'
    ).annotate(quantity=Sum('quantity'))
    purchases += '\n'.join([
        f'- {item["ingredient__name"]} '
        f'({item["ingredient__measurement_unit"]})'
        f' - {item["quantity"]}'
        for item in purchases_cart
    ])
    purchases += '\n\nFoodgram'
    response = HttpResponse(purchases, content_type='application/pdf')
    filename = f'{request.user.username}_shopping_list.pdf'
    response['Content-Disposition'] = f'attachment; filename={filename}'
    return response
