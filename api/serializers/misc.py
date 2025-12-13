from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from api.models import Product, Category, Review, FlashSale, ProductViewHistory


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ReviewSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ProductSerializer(ModelSerializer):
    avg_rating = serializers.FloatField(read_only=True,required=False)

    class Meta:
        model = Product
        fields = ['id','name','price','description','category','stock','avg_rating']


class FlashSaleSerializer(ModelSerializer):
    class Meta:
        model = FlashSale
        fields = ['id','product','discount_percentage','start_time','end_time']


class ProductViewHistorySerializer(ModelSerializer):
    class Meta:
        model = ProductViewHistory
        fields = "__all__"
