from django.db import models

# many orders for many items
# one customer for many orders
from django.utils.datetime_safe import datetime


class Item(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Customer(models.Model):
    name = models.CharField(max_length=10)
    mobile = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, related_name='orders', on_delete=models.CASCADE)
    item = models.ManyToManyField(Item, related_name='orders', through='OrderItems')
    date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.customer.__str__()


class OrderItems(models.Model):
    item = models.ForeignKey('Item', models.CASCADE)
    order = models.ForeignKey('Order', models.CASCADE)

    class Meta:
        db_table = "ordering_order_item"
