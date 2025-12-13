from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def is_in_stock(self):
        return self.stock > 0

    def reduce_stock(self,quantity):
        if quantity > self.stock:
            return False
        self.stock -= quantity
        self.save()
        return True

    def increase_stock(self,amount):
        self.stock += amount
        self.save()

    class Meta:
        ordering = ['name']



