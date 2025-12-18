from django.urls import path

from order.views import *


urlpatterns = [
    path('create', CreateOrderView.as_view()),
    path('retrieve', RetrieveOrderView.as_view()),
    path('delete/<str:id>', DeleteOrderView.as_view()),

    path('item/create', CreateOrderItemView.as_view()),
    path('item/retrieve/<str:id>', RetrieveOrderItemView.as_view()),
    path('item/update/<str:id>', UpdateOrderItemView.as_view()),
    path('item/delete/<str:id>', DeleteOrderItemView.as_view()),

]