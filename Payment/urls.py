from django.urls import path
from .views import initiate_payment, complete_payment

urlpatterns = [
    path("",initiate_payment,name="initiate_payment"),
    path("<str:ref>",complete_payment,name="complete_payment")


]