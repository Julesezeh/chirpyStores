from django.urls import path
from .views import user_cart, index, specific_product,checkout, brand_page, category_page



app_name = "MAIN"

urlpatterns = [
    path("",index,name="home"),
    path("product/<int:pk>",specific_product,name="product"),
    path("cart",user_cart,name="cart"),
    path("checkout/<int:order_id>",checkout,name="checkout"),
    path("brand/<str:brand>",brand_page,name="brand"),
    path("category/<str:category>",category_page,name="category")


]