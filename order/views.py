from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response

from order.models import Order, OrderItem
from order.serializers import *


class CreateOrderView(CreateAPIView):
    queryset = Order.gameboy.all()
    serializer_class = OrderSerializer


class CreateOrderItemView(CreateAPIView):
    queryset = OrderItem.astroboy.all()
    serializer_class = OrderItemSerializer

class RetrieveOrderItemView(RetrieveAPIView):
    queryset = OrderItem.astroboy.all()
    serializer_class = OrderItemSerializer
    lookup_field = 'id'

class UpdateOrderItemView(UpdateAPIView):
    queryset = OrderItem.astroboy.all()
    serializer_class = OrderItemSerializer
    lookup_field = 'id'

class DeleteOrderView(DestroyAPIView):
    queryset = Order.gameboy.all()
    serializer_class = OrderSerializer
    lookup_field = 'id'

class DeleteOrderItemView(DestroyAPIView):
    queryset = OrderItem.astroboy.all()
    serializer_class = OrderItemSerializer
    lookup_field = 'id'

class RetrieveOrderView(RetrieveAPIView):
    def get(self, request):
        id = request.query_params.get('id')

        try:
            order = Order.gameboy.get(id=id)
        except Exception as e:
            return Response ('order with this id is not found, sucka', status=status.HTTP_404_NOT_FOUND)
        order_items = OrderItem.astroboy.filter(order=order)
        order_items_dict = [i.get_info() for i in order_items]
        return Response(order_items_dict, status=status.HTTP_200_OK)
