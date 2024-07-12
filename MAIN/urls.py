from django.urls import path
from .views import user_cart, index, specific_product,checkout



app_name = "MAIN"

urlpatterns = [
    path("",index,name="home"),
    path("product/<int:pk>",specific_product,name="product"),
    path("cart",user_cart,name="cart"),
    path("checkout/<int:order_id>",checkout,name="checkout")


]