from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from . forms import PaymentForm
from .models import Order, Payment
from django.contrib.auth.decorators import login_required


# Create your views here.



# For the payment handlers, once payment is successful, update the amount of Product/items available in stock

# def initiate_payment(request):
#     if request.method == "POST":
#         payment_form  = PaymentForm(request.POST)
#         if payment_form.is_valid():
#             payment = payment_form.save()
#             return render(request,"complete_payment.html",{"payment":payment})
#     else:
#         payment_form = PaymentForm()
#         return render(request,"initiate_payment.html",{"payment_form":payment_form})



# def complete_payment(request):
#     if request.method == "POST":

#     pass

@login_required
def process_payment(request,order_id):
    order = Order.objects.get(id=order_id)
    new_payment = Payment(
        order=order,
        payment_method = "paystack",
        
        )
    pass

def verify_payment(request):
    if request.method == "POST":
        pass