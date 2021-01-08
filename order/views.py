from decimal import Decimal

from agents.models import Customer
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse

from django.template.loader import render_to_string
from django.utils.crypto import get_random_string

from django.utils.timezone import localtime, now


from decimal import Decimal

from product.models import Category, Comment, Images, Product, Variants
from .models import ShopCart, Order, OrderProduct


# Create your views here.
def index(request):
   return  HttpResponse("Order Page")

def addtocart(request):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        product_id = request.POST.get("product_id")
        productdetails = Product.objects.get(pk=product_id)
        variant_id = request.POST.get("size")
        #quantity = request.POST.get("quantity")
        list = request.session["selected_customer"]
        c = Customer.objects.get(pk=list[0])

        product = Product.objects.get(pk=product_id)

        variantid_1M = variant(request.user.username, c, request.POST.get("variantid_1M"), request.POST.get("q_1M"), product_id)
        variantid_3M = variant(request.user.username, c, request.POST.get("variantid_3M"), request.POST.get("q_3M"), product_id)
        variantid_6M = variant(request.user.username, c, request.POST.get("variantid_6M"), request.POST.get("q_6M"), product_id)
        variantid_9M = variant(request.user.username, c, request.POST.get("variantid_9M"), request.POST.get("q_9M"), product_id)
        variantid_12M = variant(request.user.username, c, request.POST.get("variantid_12M"), request.POST.get("q_12M"), product_id)
        variantid_1Y = variant(request.user.username, c, request.POST.get("variantid_1Y"), request.POST.get("q_1Y"), product_id)
        variantid_2Y = variant(request.user.username, c, request.POST.get("variantid_2Y"), request.POST.get("q_2Y"), product_id)
        variantid_4Y = variant(request.user.username, c, request.POST.get("variantid_4Y"), request.POST.get("q_4Y"), product_id)
        variantid_6Y = variant(request.user.username, c, request.POST.get("variantid_6Y"), request.POST.get("q_6Y"), product_id)
        variantid_8Y = variant(request.user.username, c, request.POST.get("variantid_8Y"), request.POST.get("q_8Y"), product_id)
        variantid_10Y = variant(request.user.username, c, request.POST.get("variantid_10Y"), request.POST.get("q_10Y"), product_id)
        variantid_12Y = variant(request.user.username, c, request.POST.get("variantid_12Y"), request.POST.get("q_12Y"), product_id)
        variantid_14Y = variant(request.user.username, c, request.POST.get("variantid_14Y"), request.POST.get("q_14Y"), product_id)
        '''
        if variantid_1M is not None and variantid_1M != '':
            variant = Variants.objects.get(id=variantid_1M)
        else:
            variantid_1M = 0    
        variantid_3M = request.POST.get("variantid_3M")
        if variantid_3M is not None and variantid_3M != '':
            variant = Variants.objects.get(id=variantid_3M)
        else:
            variantid_3M = 0
        '''
        print(variantid_1M)
        print(variantid_3M)
        print(variantid_6M)
        print(variantid_9M)
        print(variantid_12M)    

        
        #variant = Variants.objects.get(id=variantid_3M)

        print(product)
        #color_id = request.POST.get('color')
        #productid = request.POST.get('productid')
        #sizes = Variants.objects.filter(product_id=productid, color_id=color_id)
        context = {
            #'added_variant': variant,
            'added_product': product,
            #'quantity': quantity
        }
        #messages.success(request, "Product has added in cart.")
        #return HttpResponseRedirect(reverse("order:shopcart"))
        data = {'rendered_table': render_to_string('agents/cart-updated.html', context=context)}
        return JsonResponse(data)
    else:
        return HttpResponse('Something went wrong!')

def addtocart_without_variant(request, product_id):
    list = request.session["selected_customer"]
    selected_customer = Customer.objects.get(pk=list[0])
    current_user = User.objects.get(username=request.user.username) 
    product_details = Product.objects.get(pk=product_id)

    print(selected_customer)
    print(current_user)
    print(product_details)
    
    if request.method == 'POST':
        q = request.POST["quantity"]

        if ShopCart.objects.filter(user_id=current_user.id, customer=selected_customer, product=product_details.id).exists():  # Check product in shopcart
            data = ShopCart.objects.get(user_id=current_user.id, customer=selected_customer, product=product_details.id)
            data.user_id = current_user.id
            data.customer = selected_customer
            data.product_id = product_details.id
            data.quantity += int(q)
            data.save()
            print(data)
            return HttpResponseRedirect(reverse("order:shopcart"))
            
        else:
            data = ShopCart()
            data.user_id = current_user.id
            data.customer = selected_customer
            data.product_id = product_details.id
            data.quantity = q
            data.save()
            print(data)
            return HttpResponseRedirect(reverse("order:shopcart"))
    else:
        return HttpResponse('Something went wrong! Please try again')


def variant(current_username, customer, v, q, p_id):
    if v is not None and v != '':
        if q != '':
            variant = Variants.objects.get(id=v)
            u = User.objects.get(username=current_username)  
            if ShopCart.objects.filter(variant_id=variant, user_id=u.id, customer=customer, product=p_id).exists():  # Check product in shopcart
                data = ShopCart.objects.get(variant_id=variant, user_id=u.id, customer=customer, product=p_id)
                data.user_id = u.id
                data.customer = customer
                data.product_id = p_id
                data.variant_id = variant.id
                data.quantity += int(q)
                data.save()
                print(data)
            else:
                data = ShopCart()
                data.user_id = u.id
                data.customer = customer
                data.product_id = p_id
                data.variant_id = variant.id
                data.quantity = q
                data.save()
                print(data)
        else:
            print('q is none')
        return v
    else:
        v = 0
        return v

def deletefromcart(request,id):
    url = request.META.get('HTTP_REFERER')
    ShopCart.objects.filter(id=id).delete()
    messages.success(request, "Your item deleted form Shopcart.")
    return HttpResponseRedirect(url)


def shopcart(request):
    list = request.session["selected_customer"]
    current_customer = Customer.objects.get(pk=list[0])
    shopcart = ShopCart.objects.filter(user_id=request.user.id, customer=current_customer)
    print(shopcart)

    total=0
    for rs in shopcart:
        total += rs.total
        print(total)

    vatTotal=0
    for vat in shopcart:
        vatTotal += vat.vattotal
        print(vatTotal)
    #return HttpResponse(str(total))
    context={
        'shopcart': shopcart,
        'total': total,
        'vatTotal': vatTotal,
        'selected_c': current_customer
    }
    return render(request,'agents/shopcart.html',context)

def orderPlace(request):
    list = request.session["selected_customer"]
    current_customer = Customer.objects.get(pk=list[0])
    current_user = User.objects.get(username=request.user.username) 
    shopcart = ShopCart.objects.filter(user_id=current_user.id , customer=current_customer.id)

    total = 0
    for t in shopcart:
        total += t.product.wholesale_price * t.quantity

    if request.method == 'POST':
        specialInstructions = request.POST.get("specialInstructions")

        data = Order()    
        data.user_id = current_user.id
        data.customer = current_customer
        ordercode = get_random_string(9).upper()
        data.code = ordercode
        t = total + (total) * 22 * Decimal(0.01)
        data.total = t
        data.ip = request.META.get('REMOTE_ADDR')
        data.note = specialInstructions
        data.save()

        for st in shopcart:
            detail = OrderProduct()
            detail.order_id = data.id
            detail.product_id = st.product_id
            detail.user_id = current_user.id
            detail.customer = current_customer
            detail.price = st.product.wholesale_price
            detail.variant_id = st.variant_id
            detail.quantity = st.quantity
            detail.total_amount = st.total
            detail.save()

        ShopCart.objects.filter(user_id=current_user.id, customer=current_customer.id).delete()
        
        return HttpResponseRedirect(reverse("order:order_completed", args=[ordercode]))
        
    else:
        messages.error(request, 'Something went wrong. Please Try again!')
        return HttpResponseRedirect(reverse("order:shopcart"))


def order_completed(request, ordercode):
    return render(request, 'agents/order_completed.html', {
            'ordercode': ordercode 
        })

def orders(request):
    current_user = User.objects.get(username=request.user.username) 
    allOrders = Order.objects.filter(user_id=current_user.id)
    return render(request, 'agents/orders_all.html', {
            'orders': allOrders 
    })

def order_detailed(request, order_id):
    current_user = User.objects.get(username=request.user.username) 
    order_details = Order.objects.get(pk=order_id)
    list_of_ordered_product = OrderProduct.objects.filter(order=order_details)
    for p in list_of_ordered_product:
        print(p)
    return render(request, 'agents/order_detailed.html', {
            'orders': order_details,
            'list_of_ordered_product': list_of_ordered_product
    })