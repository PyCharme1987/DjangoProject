from django.urls import path

from product.views import *


urlpatterns = [

    path('test', TestView.as_view()),
    path('create', CreateProductView.as_view()),
    path('list', ListProductView.as_view()),
    path('retrieve', RetrieveProductView.as_view()),
    path('update', UpdateProductView.as_view()),
    path('delete', DeleteProductView.as_view()),

]