from django.db import models
from django.utils.crypto import get_random_string


class ProductManager(models.Manager):
    def _create(self, **extra_fields):
        id = get_random_string(5)
        product = self.model(id=id, **extra_fields)
        product.save()
        return product

    def create_product(self, **extra_fields):
        return self._create(**extra_fields)

class Product(models.Model):
    class CountryChoices(models.TextChoices):
        TW = 'Taiwan'
        LA = 'Laos'
        NO = 'Norway'
        KG = 'Kyrgyzstan'
        AT = 'Austria'
        CH = 'China'

    id = models.CharField(primary_key=True, unique=True, max_length=5)
    # if no max_length is specified, its 255 by default / Can also be put to 256 or higher
    # blank and null says the DB that it can be empty / otherwise it crushes
    title = models.CharField(blank=True, null=True)
    description = models.CharField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    quantity = models.PositiveSmallIntegerField(default=0, blank=True, null=True)
    country = models.CharField(choices=CountryChoices.choices, default=CountryChoices.NO)

    objects = ProductManager()

    def get_info(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'quantity': self.quantity,
            'country': self.country
        }
