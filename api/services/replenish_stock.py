from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from api.models import Product


@extend_schema(
    summary="Admin adds stock to product",
    description="Admin replenishes product stock by a given amount.",
    parameters=[
        {
            "name": "product_id",
            "type": int,
            "location": "path",
            "required": True,
            "description": "ID of the product to replenish",
        },
        {
            "name": "amount",
            "type": int,
            "location": "path",
            "required": True,
            "description": "Amount of stock to add",
        },
    ],
    responses={
        200: dict,
        400: dict
    }
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def admin_replenish_stock(request, product_id, amount):
    """
    Admin API to replenish product stock.
    Path parameters:
        - product_id (int): ID of the product
        - amount (int): quantity to add
    """
    try:
        product = Product.objects.get(id=product_id)
        product.increase_stock(amount)

        return Response({
            'status': 'success',
            'message': f'Stock increased by {amount} for product "{product.name}"'
        }, status=status.HTTP_200_OK)

    except Product.DoesNotExist:
        return Response({
            'status': 'error',
            'message': f'Product with ID {product_id} not found'
        }, status=status.HTTP_400_BAD_REQUEST)

    except ValueError:
        return Response({
            'status': 'error',
            'message': 'Invalid input'
        }, status=status.HTTP_400_BAD_REQUEST)
