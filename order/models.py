from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string

from product.models import Product


class OrderManager(models.Manager):
    def _create(self, **extra_fields):
        id = get_random_string(7)
        order = self.model(id=id, **extra_fields)
        order.save()
        return order

    def create(self, **extra_fields):
        return self._create(**extra_fields)

# Create your models here.
class Order(models.Model):
    id = models.CharField(max_length=7, primary_key=True, unique=True)
    created_at = models.DateTimeField(default=timezone.now)

    gameboy = OrderManager()

    def get_info(self):
        return {
            'id': self.id,
            'created_at': self.created_at,
        }


class OrderItemManager(models.Manager):
    def _create(self, **extra_fields):
        id = get_random_string(10)
        order_item = self.model(id=id, **extra_fields)
        order_item.save()
        return order_item

    def create(self, **extra_fields):
        product = extra_fields.get('product')
        quantity = extra_fields.get('quantity')

        price = product.price * quantity
        extra_fields.update({
            'price': price
        })
        return self._create(**extra_fields)


class OrderItem(models.Model):
    id = models.CharField(max_length=10, primary_key=True, unique=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    astroboy = OrderItemManager()

    def get_info(self):
        return {
            'id': self.id,
            'product': self.product.get_info() if self.product else None, # self.null.get_info
            'order': self.order.get_info(),
            'quantity': self.quantity,
            'price': self.price
        }