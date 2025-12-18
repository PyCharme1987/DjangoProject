from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from product.serializers import *


class TestView(APIView):
    def get(self, request):
        print('its working')
        return Response('its workinggg', 200)


class CreateProductView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post (self, request):
        # print(request)
        print(request.data)
        data = request.data
        serializer = CreateProductSerializer(data=data)
        if serializer.is_valid(raise_exception=True): #.is_valid automatically calls all functions that contain the word validate
            serializer.create(serializer.validated_data)

        return Response('still working', status=status.HTTP_200_OK)

class ListProductView(APIView):
    def get(self, request):
        products = Product.objects.all() #query set
        product_dicts = [i.get_info() for i in products] # List Comprehension


        return Response(product_dicts, status=status.HTTP_200_OK)

class RetrieveProductView(APIView):
    def get(self, request):
        id = request.query_params.get('id')
        try:
            product = Product.objects.get(id=id)
            return Response(product.get_info(), status=status.HTTP_200_OK)
        except Exception as e:
            return Response('product with this id is not found, sucking sucher', status=status.HTTP_204_NO_CONTENT)

class UpdateProductView(APIView):
    def patch(self, request):
        id = request.query_params.get('id')
        try:
            product = Product.objects.get(id=id)
        except Exception as e:
            return Response('product with this id is not found sugar', status=status.HTTP_404_NOT_FOUND)
        data = request.data
        serializer = UpdateProductSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            updated_product = serializer.update(product, serializer.validated_data)
        return Response(updated_product.get_info(), status=status.HTTP_200_OK)

class DeleteProductView(APIView):
    def delete(self, request):
        id = request.query_params.get('id')
        try:
            product = Product.objects.get(id=id)
            product.delete()
            return Response('product with this id has been deleted', status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return Response('product with this id is not found sugar sucker', status=status.HTTP_404_NOT_FOUND)
