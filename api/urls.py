from . import signals

from django.urls import path, include
from rest_framework import routers
from .views import ProductViews, CategoryViews, ReviewViews, OrderViewSet
from api.services.flash_sale import FlashSaleListCreateView, CheckFlashSale
from api.services.product_view_history import ProductViewHistoryCreated
from api.services.replenish_stock import admin_replenish_stock

from billing.views import CreateChargeView

router = routers.DefaultRouter()
router.register(r'category', CategoryViews)
router.register(r'product', ProductViews)
router.register(r'review', ReviewViews)
router.register(r'order', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),

    path('sale/', FlashSaleListCreateView.as_view()),
    path('check-sale/<int:product_id>/', CheckFlashSale.as_view()),
    path('product-view/', ProductViewHistoryCreated.as_view()),


    path('admin/replenish_stock/<int:product_id>/<int:amount>/', admin_replenish_stock),
    path('payment/charge/', CreateChargeView.as_view(), name='stripe-charge'),

]
