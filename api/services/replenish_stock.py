from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework import status

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse

from api.models import Product


@extend_schema(
    summary="Admin replenishes product stock",
    description="Admin mahsulot stokini ko‘paytiradi",
    parameters=[
        OpenApiParameter(
            name="amount",
            description="Qancha miqdorda stok qo‘shiladi",
            required=True,
            type=int,
            location=OpenApiParameter.PATH
        ),
        OpenApiParameter(
            name="product_id",
            description="Mahsulot ID",
            required=True,
            type=int,
            location=OpenApiParameter.PATH
        ),
    ],
    responses={
        200: OpenApiResponse(
            description="Stock muvaffaqiyatli qo‘shildi",
            response={
                "type": "object",
                "properties": {
                    "status": {"type": "string"},
                    "message": {"type": "string"},
                    "stock_qty": {"type": "number"}
                }
            }
        ),
        404: OpenApiResponse(description="Product topilmadi"),
        400: OpenApiResponse(description="Noto‘g‘ri input"),
    }
)
@api_view(["POST"])
@permission_classes([IsAdminUser])
def admin_replenish_stock(request, product_id, amount):
    """
    POST /api/admin/products/{product_id}/replenish/{amount}/
    """
    product = get_object_or_404(Product, id=product_id)

    if amount <= 0:
        return JsonResponse(
            {"status": "error", "message": "amount musbat bo‘lishi kerak"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Oddiy stok oshirish
    product.increase_stock(amount)
    product.save()

    return JsonResponse({
        "status": "success",
        "message": f"Stock {amount} ga oshirildi",
        "stock_qty": product.stock_qty
    })
