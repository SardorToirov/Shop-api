from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.db import transaction

import stripe

from .models import Payment
from api.models import Order

stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateChargeView(APIView):
    def post(self, request, *args, **kwargs):
        stripe_token = request.data.get("stripe_token")
        order_id = request.data.get("order_id")

        if not stripe_token or not order_id:
            return Response(
                {"error": "stripe_token and order_id required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Orderni tekshirish
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response(
                {"error": "Order not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if order.is_paid:
            return Response(
                {"error": "Order already paid"},
                status=status.HTTP_400_BAD_REQUEST
            )

        total_amount = order.product.price * order.quantity

        try:
            # Stripe charge
            charge = stripe.Charge.create(
                amount=int(total_amount * 100),  # cents
                currency="usd",
                source=stripe_token,
                description=f"Order #{order.id}"
            )

            # MUHIM: atomic transaction
            with transaction.atomic():
                Payment.objects.create(
                    order=order,
                    stripe_charge_id=charge["id"],
                    amount=total_amount,
                    status="success"
                )
                # ❌ order.is_paid bu yerda YO‘Q
                # ✅ signal orqali qilinadi

            return Response(
                {"status": "Payment successful"},
                status=status.HTTP_201_CREATED
            )

        except stripe.error.CardError as e:
            return Response(
                {"error": e.user_message},
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
