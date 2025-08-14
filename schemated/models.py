from django.db import models
from .mixins import PricingMixin

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'schema_one"."customer'


class Order(PricingMixin):
    order_number = models.CharField(max_length=50)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    class Meta:
        db_table = 'schema_two"."order'

class PreOrder(PricingMixin):
    order_number = models.CharField(max_length=50)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    class Meta:
        db_table = 'schema_one"."pre_order'