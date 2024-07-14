from django.urls import path
from .views import process_payment

app_name = "payment"

urlpatterns = [
    # path("",initiate_payment,name="initiate_payment"),
    # path("<str:ref>",complete_payment,name="complete_payment")
    path("process_payment/<str:order_id>",process_payment,name='process_payment')

]