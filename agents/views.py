from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.models import User

from django.utils.timezone import localtime, now

from .models import Customer
from product.models import Category, Product, Images, Comment, Variants

#from django.contrib.auth.models import User
#settings.AUTH_USER_MODEL



# Create your views here.

def index(request):
    if request.method == "POST":
        username = request.POST["username"]
        userpass = request.POST["inputPass"]
        
        user = authenticate(username=username, password=userpass)

        if user:
            login(request, user)
            agent_name = request.user.username
            return HttpResponseRedirect(reverse("agents:agent", args=[agent_name]))
        else:
            return render(request, "agents/index.html", {
                "message" : "Email or password is incorrect!"
            })        
    else:
        logout(request)
        return render(request, "agents/index.html")

def agent(request, agent_name):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("agents:index"))
    else:
        user = request.user
        return render(request, "agents/agent.html", {
            "user": user
        })    

def customers(request, agent_name):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("agents:index"))
    else:
        user = request.user
        customers = Customer.objects.filter(created_by=user)
        #.all()

        if request.method == "POST":
            selected_customer = request.POST["customer"]
            request.session["selected_customer"] = [selected_customer]
            return HttpResponseRedirect(reverse("agents:products"))

        return render(request, "agents/customers.html", {
            "user": user,
            "agent_name": agent_name,
            "customers": customers
        }) 

def products(request):
    if not request.user.is_authenticated:
        if "selected_customer" not in request.session:
            request.session["selected_customer"] = []
        
        return HttpResponseRedirect(reverse("agents:index"))
    else:
        list = request.session["selected_customer"]
        c = Customer.objects.get(pk=list[0])
        user = request.user
        if request.method == 'GET':
            query = request.GET.get('q', None)
            if query:
                latest_products = Product.objects.filter(title__icontains=query)
                return render(request, "agents/products.html", {
                    
                    "user": user,
                    "selected_c": c,
                    "latest_products": latest_products

                })
            else:
                latest_products = Product.objects.all()
                return render(request, "agents/products.html", {
                    "user": user,
                    "selected_c": c,
                    "latest_products": latest_products

                })    
                #template = loader.get_template()
        else:    
            #context = Context({ 'query': query, 'results':results })
            latest_products = Product.objects.all().order_by('-id')[:4]
            return render(request, "agents/products.html", {
            "user": user,
            "selected_c": c,
            "latest_products": latest_products

            })
        latest_products = Product.objects.all().order_by('-id')[:4]
        return render(request, "agents/products.html", {
            "user": user,
            "selected_c": c,
            "latest_products": latest_products

        })    

def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Product.objects.filter(title__icontains=query)
        else:
            return Product.objects.all()

def detailed_product(request, product_id):
    list = request.session["selected_customer"]
    c = Customer.objects.get(pk=list[0])
    user = request.user
    product = Product.objects.get(pk=product_id)
    v = Variants.objects.filter(product=product_id)
    variants = Variants.objects.filter(product_id=product_id)

    colors = Variants.objects.filter(product_id=product_id,size_id=variants[0].size_id )
    sizes = Variants.objects.raw('SELECT * FROM  product_variants  WHERE product_id=%s GROUP BY size_id',[product_id])
    variant =Variants.objects.get(id=variants[0].id)
    return render(request, "agents/detailed-product.html", {
        "user": user,
        "selected_c": c,
        "product" : product,
        'sizes': sizes, 
        'colors': colors,
        'vt': v,
        'variant': variant
    })
    
def orders(request):
    list = request.session["selected_customer"]
    c = Customer.objects.get(pk=list[0])
    user = request.user
    return render(request, "agents/detailed-product.html", {
        "user": user,
        "selected_c": c
    })    

def analytics(request):
    return HttpResponse("analytics")

def settings(request):
    return HttpResponse("settings")

def doLogout(request):
    logout(request)
    return render(request, "agents/index.html", {
        "message": "Logged Out"
    })   

def add_customer(request, agent_name):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("agents:index"))
    else:
        if request.method == "POST":
            name = request.POST["name"]
            email = request.POST["email"]
            phone = request.POST["phone"]
            region = request.POST["region"]
            billing_address = request.POST["billing_address"]
            delivery_address = request.POST["delivery_address"]
            vat_number = request.POST["vat_number"]
            
            u = User.objects.get(username=agent_name)
            c = Customer(name=name, email=email, phone=phone, region=region, billing_address=billing_address, delivery_address=delivery_address, vat_number=vat_number, pub_date=localtime(now()), created_by=u)
            c.save()
            return HttpResponseRedirect(reverse("agents:customers", args=[agent_name]))

        user = request.user
        return render(request, "agents/add-customer.html", {
            "user": user,
            "agent_name": agent_name
        })