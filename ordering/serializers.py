from django.db import transaction
from rest_framework import serializers
from ordering.models import Customer, Item, Order, OrderItems


class ItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField()

    class Meta:
        model = Item
        fields = ['id', 'name']
        depth = 1


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'mobile', 'orders']
        depth = 1


class CustomersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['name', 'mobile']
        depth = 1


class OrderSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    customer_id = serializers.IntegerField(required=True)
    item = ItemSerializer(many=True, required=True)

    class Meta:
        model = Order
        fields = ['id', 'date', 'customer_id', 'item', ]

    def create(self, validated_data):
        item_data = validated_data.pop('item', [])
        with transaction.atomic():
            order = Order(**validated_data)
            order.save()
            through = order.item.through
            objects = []
            for item in item_data:
                objects.append(through(item_id=item["id"], order_id=order.id))
            through.objects.bulk_create(objects)
        return order

    def update(self, instance, validated_data):
        items_data = validated_data.pop('item', None)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        if items_data is not None:
            OrderItems.objects.filter(order=instance).delete()
            for item in items_data:
                OrderItems.objects.create(order=instance, item_id=item['id'])
        return instance


class OrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = ['item']
