from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from . forms import PaymentForm

# Create your views here.



# For the payment handlers, once payment is successful, update the amount of Product/items available in stock

def initiate_payment(request):
    if request.method == "POST":
        payment_form  = PaymentForm(request.POST)
        if payment_form.is_valid():
            payment = payment_form.save()
            return render(request,"complete_payment.html",{"payment":payment})
    else:
        payment_form = PaymentForm()
        return render(request,"initiate_payment.html",{"payment_form":payment_form})



def complete_payment(request):
    pass