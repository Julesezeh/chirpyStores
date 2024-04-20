from django.shortcuts import render, get_object_or_404, redirect
from .models import BasePopup, Product
from Payment.models import Order, OrderItem
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.contrib import messages
from django.http import JsonResponse


# Create your views here.



# When rendering the products individually, the maximum the user should be able to order should match the number available
# And updated immediately using HTMX
def index(request):
    categories = ["Accessories","Sports & Entertainment","Home & Garden", "Hair Extensions & Wigs","Men's Clothing","Consumer Electronics", "Home Appliances"]
    products = Product.objects.all()

    if request.user.is_authenticated:
        user_orders = Order.objects.filter(user=request.user,is_active=True).last()
        user_order_items = OrderItem.objects.filter(order = user_orders)
        number_of_orders = len(user_order_items)
        print(number_of_orders)
    else: number_of_orders = None
    return render(request, 'index-final.html',{'categories':categories,"slime":"wowzer-style","products":products,"quantity":number_of_orders})



def user_cart(request):
    categories = ["Accessories","Sports & Entertainment","Home & Garden", "Hair Extensions & Wigs","Men's Clothing","Consumer Electronics", "Home Appliances"]
    user_current_order = Order.objects.filter(user = request.user, is_active=True).last()
    user_order_items = OrderItem.objects.filter(order=user_current_order)
    # cart_items = Order.objects.filter(user=request.user )
    return render(request,'cart-final.html',{'categories':categories, 'order_items':user_order_items, 'current_order':user_current_order})



def specific_product(request,pk):
    product = get_object_or_404(Product,pk=pk)
    if request.user.is_authenticated:
        user_orders = Order.objects.filter(user=request.user,is_active=True).last()
        user_order_items = OrderItem.objects.filter(order=user_orders)
        number_of_orders = len(user_order_items)
        print(number_of_orders)
    else: number_of_orders = None    
    return render(request, "product.html", {"product":product,"quantity":number_of_orders})


@login_required
def add_to_cart(request):
    if request.method == "POST": 
        if request.user.is_authenticated:
            print(request.POST)
            user = request.user
            quantity = request.POST.get("quantity") 
            print("quantity")
            int_quantity = int(quantity)
            
            product_id = request.POST.get("product")

            product = get_object_or_404(Product,pk=product_id)


             #debug
            # print("product_price", product.price, type(float(product.price)))
            # print("quantity",quantity, type(float(quantity)))


            # Calculate line total            
            line_total = float(product.price) * float(quantity)

            # Retrieve or create the user's order
            order, created = Order.objects.get_or_create(user=user, is_active=True)
            
            order_item, created = OrderItem.objects.get_or_create(order=order, product=product)

            if created:
                print("Order created: ", order)

                try:
                    # Create or update the order item
                    order_item.quantity += int_quantity
                    order_item.line_total += line_total
                    order_item.save()
                    print("Order item saved from try block")
                    # Update the total amount of the order
                    order.save()
                    order.save_and_update_total_amount()
                    print("Order saved from try block")

                except TypeError as e:
                    print("Error!")
                    print(e)
 

            else:
                print("Order fetched: ", order)
                try:
                    # Create or update the order item
                    order_item.quantity += int_quantity
                    order_item.line_total += line_total
                    order_item.save()
                    # Update the total amount of the order
                    order.total_amount += line_total
                    order.save()
                    print("Order and Order item saved from try block")

                except TypeError as e:
                    print("Error!")
                    print(e)


            # messages.success(request,message="Added to cart")

            
            user_orders = Order.objects.filter(user=request.user,is_active=True).last()
            user_order_items = OrderItem.objects.filter(order=user_orders)

            number_of_orders = len(user_order_items)
            print(number_of_orders)
            
            return  render(request,'partials/cart-count.html',{"quantity":number_of_orders})
        
        else:
            return redirect("/auth/login")
        
    else:
        return redirect("/auth/login")




def remove_from_cart(request,pk):
    order_item = OrderItem.objects.filter(id=pk)
    order = Order.objects.filter(user=request.user, is_active=True).last()

    order.total_amount -= order_item[0].line_total
    deleted_order  = order_item.delete()
    order.save_and_update_total_amount()

    current_order = Order.objects.filter(user=request.user).last()
    current_order_items = OrderItem.objects.filter(order=order)
    number_of_orders = len(current_order_items)

    if not current_order_items:
        current_order.is_active=False
    return render(request, 'partials/cart-items.html',{'order_items':current_order_items,"quantity":number_of_orders,'current_order':order})


def update_order_item(request,pk):
    if request.method == "POST":
        order_item = OrderItem.objects.get(id=pk)
        quantity = int(request.POST.get("quantity"))

        if quantity < order_item.quantity:
            new_total = float(quantity) * order_item.product.price 

            order_item.quantity -= (order_item.quantity-quantity)
            order_item.line_total = new_total

            order_item_order = order_item.order
            order_item.save()
            order_item_order.save_and_update_total_amount()

            current_order_items = OrderItem.objects.filter(order=order_item_order)

        elif quantity > order_item.quantity:
            new_total = float(quantity) * order_item.product.price 

            order_item.quantity += (quantity-order_item.quantity)
            order_item.line_total = new_total
            order_item_order = order_item.order

            order_item.save()
            order_item_order.save_and_update_total_amount()

            current_order_items = OrderItem.objects.filter(order=order_item_order)



        return render(request,'partials/cart-items.html',{"order_items":current_order_items,"current_order":order_item_order})



def checkout(request):
    return render(request,'checkout.html')