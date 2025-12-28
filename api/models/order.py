from django.contrib.auth.models import User
from django.db import models
from .product import Product
from django.core.validators import RegexValidator

phone_regex = RegexValidator(
    regex=r'^\+998\d{9}$',
    message="Phone number must be in the format: '998xxxxxxxxx'."
)


class Order(models.Model):
    PENDING = 'Pending'
    PROCESSING = 'Processing'
    SHIPPED = 'Shipped'
    DELIVERED = 'Delivered'
    CANCELED = 'Canceled'

    STATUS_CHOICE = [
        (PENDING, 'Pending'),
        (PROCESSING, 'Processing'),
        (SHIPPED, 'Shipped'),
        (DELIVERED, 'Delivered'),
        (CANCELED, 'Canceled'),
    ]

    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    customer = models.ForeignKey(User,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICE,
        default=PENDING,
    )
    phone_number = models.CharField(validators=[phone_regex],max_length=13)

    @property
    def total_price(self):
        return self.product.price * self.quantity

    def set_status(self,new_status):
        if new_status not in dict(self.STATUS_CHOICE):
            raise ValueError("Invalid status!!!")
        self.status = new_status
        self.save()

    def is_transition_allowed(self,new_status):
        allow_transition = {
            self.PENDING: [self.PROCESSING,self.CANCELED],
            self.PROCESSING: [self.SHIPPED,self.CANCELED],
            self.SHIPPED: [self.DELIVERED,self.CANCELED]
        }

        return new_status in allow_transition.get(self.status,[])

    def __str__(self):
        return f"Order ( {self.product.name} by {self.customer.username} )"
