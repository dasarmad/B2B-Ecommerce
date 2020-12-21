from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = "agents"
urlpatterns = [
    path("", views.index, name="index"),
    path("agent/<str:agent_name>/orders/", views.agent, name="agent"),
    path("agent/<str:agent_name>/customers/", views.customers, name="customers"),
    path("agent/<str:agent_name>/add-customer/", views.add_customer, name="add_customer"),
    path("agent/products/", views.products, name="products"),
    path("agent/products/<int:product_id>", views.detailed_product, name="detailed_product"),
    path("products/orders/", views.orders, name="orders"),
    path("", views.doLogout, name="doLogout"),
    path("logout/", LogoutView.as_view(), name="logout")    
]