from rest_framework import serializers

from order.models import Order, OrderItem


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = []


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'order', 'quantity', 'id', 'price']
        extra_kwargs = {
            'price': {'read_only': True},
            'id': {'read_only': True},
        }

    def update(self, instance, validated_data):
        quantity = validated_data.get('quantity', instance.quantity)
        product = validated_data.get('product', instance.product)

        price = quantity * product.price

        validated_data.update({
            'price':price
        })

        return super().update(instance, validated_data)