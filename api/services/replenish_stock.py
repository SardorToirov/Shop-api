from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework import status
from api.models import Product


@api_view(["POST"])
@permission_classes([IsAdminUser])
def admin_replenish_stock(request, product_id, amount):
    product = get_object_or_404(Product, id=product_id)

    if amount <= 0:
        return JsonResponse(
            {"message": "amount musbat bo‘lishi kerak"},
            status=status.HTTP_400_BAD_REQUEST
        )

    product.increase_stock(amount)

    return JsonResponse({
        "message": f"Stock {amount} ga oshirildi",
        "stock": product.stock
    })
