from django.urls import path, include
from rest_framework import routers
from .views import ProductViews, CategoryViews, ReviewViews
from api.services.flash_sale import FlashSaleListCreateView,CheckFlashSale
from api.services.product_view_history import ProductViewHistoryCreated

router = routers.DefaultRouter()
router.register(r'category', CategoryViews)
router.register(r'product', ProductViews)
router.register(r'review', ReviewViews)

urlpatterns = [
    path('', include(router.urls)),

    path('sale/',FlashSaleListCreateView.as_view()),
    path('chack-sale/<int:product_id>/',CheckFlashSale.as_view()),
    path('product-view/',ProductViewHistoryCreated.as_view())

]
