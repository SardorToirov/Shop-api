from api.models import Product, FlashSale, ProductViewHistory
from api.serializers import FlashSaleSerializer
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime, timedelta
from api.filters import FalshFilter
from rest_framework.pagination import PageNumberPagination
from django_filters import rest_framework as django_filters

class CustomPagination(PageNumberPagination):
    page_size = 4


class FlashSaleListCreateView(generics.ListCreateAPIView):
    queryset = FlashSale.objects.all()
    serializer_class = FlashSaleSerializer

    pagination_class = CustomPagination
    filter_backends = (django_filters.DjangoFilterBackend,)
    filterset_class = FalshFilter

class CheckFlashSale(APIView):
    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=404)

        viewed = ProductViewHistory.objects.filter(
            user=request.user,
            product=product
        ).exists()

        sale = FlashSale.objects.filter(
            product=product,
            start_time__lte=datetime.now() + timedelta(hours=24)
        ).first()

        if viewed and sale:
            return Response({
                "message": f"{sale.discount_percentage}% chegirma bo‘ladi!",
                "start_time": sale.start_time,
                "end_time": sale.end_time
            })

        return Response({"message": "Aksiya yo‘q"})
