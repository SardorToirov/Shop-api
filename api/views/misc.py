from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response


from api.serializers import ProductSerializer,CategorySerializer,ReviewSerializer,OrderSerializers
from rest_framework.pagination import PageNumberPagination
from django_filters import rest_framework as django_filters
from ..filters import ProductFilter
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated

from ..models import Category, Review, Product,Order


# Create your views here.


class CategoryViews(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ['name']


class ReviewViews(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class CustomPagination(PageNumberPagination):
    page_size = 4


class ProductViews(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    pagination_class = CustomPagination
    filter_backends = (django_filters.DjangoFilterBackend,filters.SearchFilter)
    filterset_class = ProductFilter
    search_fields = ['name', 'description']

    def list(self, request, *args, **kwargs):
        category = request.query_params.get('category',None)
        if category:
            self.queryset = self.queryset.filter(category=category)
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        related_products = Product.objects.filter(category=instance.category).exclude(id=instance.id)[:5]
        related_serializer = ProductSerializer(related_products,many=True)
        return Response({
            'product':serializer.data,
            'related_products':related_serializer.data
        })


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = Order.objects.all()
    serializer_class = OrderSerializers

