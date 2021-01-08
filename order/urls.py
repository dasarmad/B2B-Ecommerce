from django.urls import path

from . import views

app_name = "order"

urlpatterns = [
    path('', views.index, name='index'),
    path('addtocart/', views.addtocart, name='addtocart'),
    path('addtocart_w_v/<int:product_id>', views.addtocart_without_variant, name='addtocart_without_variant'),
    path('shopcart/', views.shopcart, name='shopcart'),
    path('deletefromcart/<int:id>', views.deletefromcart, name='deletefromcart'),
    path('orderPlace/', views.orderPlace, name='orderPlace'),
    path('order_completed/<str:ordercode>', views.order_completed, name='order_completed'),
    path('all-orders/', views.orders, name='orders'),
    path('order-details/<int:order_id>', views.order_detailed, name='order_detailed')
]