from django.db.models.signals import post_save
from django.dispatch import receiver

from billing.models import Payment
from .models import Order
from .tasks import send_telegram_notification


@receiver(post_save, sender=Order)
def notify_admin(sender, instance, created, **kwargs):
    if created:
        send_telegram_notification.delay(
            order_id=instance.id,
            product_name=instance.product.name,
            quantity=instance.quantity,
            customer_username=instance.customer.username,
            phone_number=instance.phone_number
        )


@receiver(post_save, sender=Payment)
def mark_order_as_paid(sender, instance, created, **kwargs):
    if created and instance.status == "success":
        order = instance.order
        order.is_paid = True
        order.save()
