from django.shortcuts import render, get_object_or_404, redirect
from .models import BasePopup, Product,ShoeBrand,ProductCategory
from Payment.models import Order, OrderItem, BillingInformation
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.contrib import messages
from django.http import JsonResponse
import time
import chirpyStores.settings as settings


# Create your views here.



# When rendering the products individually, the maximum the user should be able to order should match the number available
# And updated immediately using HTMX
def index(request):
    # categories = ["Accessories","Sports & Entertainment","Home & Garden", "Hair Extensions & Wigs","Men's Clothing","Consumer Electronics", "Home Appliances"]
    products = Product.objects.all()
    brands = ShoeBrand.objects.all()
    categories = ProductCategory.objects.all()    



    if request.user.is_authenticated:
        user_orders = Order.objects.filter(user=request.user,is_active=True).last()
        user_order_items = OrderItem.objects.filter(order = user_orders)
        number_of_orders = len(user_order_items)
        print(number_of_orders)
    else: number_of_orders = None
    return render(request, 'index-final.html',{'categories':categories,"slime":"wowzer-style",'brands':brands,"products":products,"quantity":number_of_orders})


@login_required
def user_cart(request):
    categories = ["Accessories","Sports & Entertainment","Home & Garden", "Hair Extensions & Wigs","Men's Clothing","Consumer Electronics", "Home Appliances"]
    user_current_order = Order.objects.filter(user = request.user, is_active=True).last()
    user_order_items = OrderItem.objects.filter(order=user_current_order)
    brands = ShoeBrand.objects.all()

    # cart_items = Order.objects.filter(user=request.user )
    return render(request,'cart-final.html',{'categories':categories,'brands':brands, 'order_items':user_order_items, 'current_order':user_current_order})



def specific_product(request,pk):
    product = get_object_or_404(Product,pk=pk)
    brands = ShoeBrand.objects.all()

    if request.user.is_authenticated:
        user_orders = Order.objects.filter(user=request.user,is_active=True).last()
        user_order_items = OrderItem.objects.filter(order=user_orders)
        number_of_orders = len(user_order_items)
        print(number_of_orders)
    else: 
        number_of_orders = None    
    return render(request, "product.html", {"product":product,"quantity":number_of_orders,'brands':brands})


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
        
        time.sleep(2)

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


def save_billing_info(request):
    if request.method == "POST":
        print("Save View Triggered")
        # Using indicator to determine if the POST request is coming from the else statement or the new billing info modal
        main_indicator = request.POST.get("from_else_statement")
        aux_indicator = request.POST.get("from_modal")
        if main_indicator:
            delivery_email = request.POST.get("email-n")
            delivery_first_name = request.POST.get("first_name-n")
            delivery_last_name = request.POST.get("last_name-n")
            delivery_street_address = request.POST.get("street_address-n")
            delivery_city = request.POST.get("city-n")
            delivery_state = request.POST.get("state-n")
            delivery_notes = request.POST.get("notes-n",None)
            new_billing_info = BillingInformation(user=request.user,
                                                first_name=delivery_first_name,
                                                last_name=delivery_last_name,
                                                email=delivery_email,
                                                street_address=delivery_street_address,
                                                city=delivery_city,
                                                state=delivery_state,
                                                notes=delivery_notes)
            new_billing_info.save()

            user = request.user
            # print(user.email)
            paystack_public_key = settings.PAYSTACK_PUBLIC_KEY
            user_current_order = Order.objects.filter(user = user, is_active=True).last()
            user_order_items = OrderItem.objects.filter(order=user_current_order)
            delivery_details = BillingInformation.objects.filter(user=request.user)

            print(user_order_items)
            return render(request,'checkout.html',{"order_items":user_order_items, 'current_order':user_current_order,'delivery_details':delivery_details, "public_key":paystack_public_key, "user":user})
        
        elif aux_indicator:
            delivery_email = request.POST.get("email-n")
            delivery_first_name = request.POST.get("first_name-n")
            delivery_last_name = request.POST.get("last_name-n")
            delivery_street_address = request.POST.get("street_address-n")
            delivery_city = request.POST.get("city-n")
            delivery_state = request.POST.get("state-n")
            delivery_notes = request.POST.get("notes-n",None)
            new_billing_info = BillingInformation(user=request.user,
                                                first_name=delivery_first_name,
                                                last_name=delivery_last_name,
                                                email=delivery_email,
                                                street_address=delivery_street_address,
                                                city=delivery_city,
                                                state=delivery_state,
                                                notes=delivery_notes)
            new_billing_info.save()

            user = request.user
            # print(user.email)
            # paystack_public_key = settings.PAYSTACK_PUBLIC_KEY
            # user_current_order = Order.objects.filter(user = user, is_active=True).last()
            # user_order_items = OrderItem.objects.filter(order=user_current_order)
            delivery_details = BillingInformation.objects.filter(user=request.user)


            print(user_order_items)
            return render(request,'partials/delivery_info.html',{'delivery_details':delivery_details})

@login_required
def checkout(request,order_id):
    # if request.method == "POST":
    #     existing_billing_info_pk = request.POST.get("delivery_info")
    #     if existing_billing_info_pk:
    #         selected_choice = BillingInformation.objects.get(pk=existing_billing_info_pk)
    #         user_current_order = Order.objects.filter(user = request.user, is_active=True).last()
    #         user_current_order.billing_info = selected_choice
    #         user_current_order.save()

    #     else:
    #         delivery_email = request.POST.get("email")
    #         delivery_first_name = request.POST.get("first_name")
    #         delivery_last_name = request.POST.get("last_name")
    #         delivery_street_address = request.POST.get("street_address")
    #         delivery_city = request.POST.get("city")
    #         delivery_state = request.POST.get("state")
    #         delivery_notes = request.POST.get("notes",None)
    #         new_billing_info = BillingInformation(user=request.user,
    #                                             first_name=delivery_first_name,
    #                                             last_name=delivery_last_name,
    #                                             email=delivery_email,
    #                                             street_address=delivery_street_address,
    #                                             city=delivery_city,
    #                                             state=delivery_state,
    #                                             notes=delivery_notes)
    #         new_billing_info.save()
    #         user_current_order = Order.objects.filter(user = request.user, is_active=True).last()
    #         user_current_order.billing_info = new_billing_info
    #         user_current_order.save()

    # Create a new Payment for the Order that's about to be processed if no payment exists already       
    user_current_order = Order.objects.get(pk=order_id)
    user = request.user
    # print(user.email)
    paystack_public_key = settings.PAYSTACK_PUBLIC_KEY
    user_order_items = OrderItem.objects.filter(order=user_current_order)
    delivery_details = BillingInformation.objects.filter(user=request.user)
    brands = ShoeBrand.objects.all()


    print(user_order_items)
    return render(request,'checkout.html',{"order_items":user_order_items, 'current_order':user_current_order,'delivery_details':delivery_details, "public_key":paystack_public_key, "user":user, 'brands':brands})





def brand_page(request,brand):
    brand_ = ShoeBrand.objects.get(name=brand)
    #The second and third queries are for the data in the brands and category dropdowns in the navbar
    brands = ShoeBrand.objects.all()
    categories = ProductCategory.objects.all()    
    if brand and brand_:
        products = Product.objects.filter(brand=brand_.pk)
    return render(request,'categories.html',{'brand':brand,'categories':categories, 'products':products,'brands':brands})

def category_page(request,category):
    category_ = ProductCategory.objects.get(name=category)
    #The second and third queries are for the data in the brands and category dropdowns in the navbar
    brands = ShoeBrand.objects.all() 
    categories = ProductCategory.objects.all()

    if category and category_ :
        products = Product.objects.filter(category=category_.pk)
        return render(request,'categories.html',{'category':category,'products':products,'categories':categories,'brands':brands})
    


def search_results(request):
    # Search through Product names, ProductCategory names and Brand names, and conditionally render them on a search results page
    if request.method == "POST":
        text = request.POST.get("query")
        if text:
            query_filter = text.lower()
            # Product Search
            related_products = Product.objects.filter(name__contains=query_filter)
            related_brands = ShoeBrand.objects.filter(name__contains=query_filter)
            related_categories = ProductCategory.objects.filter(name__contains=query_filter)
            print({"related_products":related_products, "related_brands":related_brands,"related_categories":related_categories})
            return render(request,'search_results.html',context={'related_brands':related_brands,'related_categories':related_categories,'related_products':related_products})