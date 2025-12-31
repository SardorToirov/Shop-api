from django.db import models
from api.models import Order

class Payment(models.Model):
    # To'lov holatlari uchun variantlar
    STATUS_CHOICES = (
        ('pending', 'Kutilmoqda'),
        ('success', 'Muvaffaqiyatli'),
        ('failed', 'Xato'),
    )

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    stripe_charge_id = models.CharField(max_length=100)
    # DecimalField pul miqdori uchun eng to'g'ri tanlov
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.stripe_charge_id} for Order {self.order.id}"