from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse

from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models.query import QuerySet

from django.template.loader import render_to_string

from django.utils.timezone import localtime, now

from .models import Customer
from product.models import Category, Product, Images, Comment, Variants, Color
from order.models import ShopCart

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

def redirectToProducts(request, customer_id):
    request.session["selected_customer"] = [customer_id]
    return HttpResponseRedirect(reverse("agents:products"))

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

def detailed_product(request, id, slug):
    query = request.GET.get('query')
    list = request.session["selected_customer"]
    c = Customer.objects.get(pk=list[0])
    user = request.user
    category = Category.objects.all()

    product = Product.objects.get(pk=id)

    images = Images.objects.filter(product_id=id)
    comments = Comment.objects.filter(product_id=id,status='True')
    context = {'product': product,'category': category,
               'images': images, 'comments': comments, "selected_c": c,
               }
    if product.variant !="None": # Product have variants
        if request.method == 'POST': #if we select color
            variant_id = request.POST.get('variantid')
            variant = Variants.objects.get(id=variant_id) #selected product by click color radio
            colors = Variants.objects.raw('SELECT * FROM  product_variants  WHERE product_id=%s GROUP BY color_id',[id])
            #colors = Variants.objects.filter(product_id=id,size_id=variant.size_id )
            sizes = Variants.objects.filter(product_id=id,color_id=variant.color_id)
            query += variant.title+' Size:' +str(variant.size) +' Color:' +str(variant.color)
        else:
            variants = Variants.objects.filter(product_id=id)
            colors = Variants.objects.raw('SELECT * FROM  product_variants  WHERE product_id=%s GROUP BY color_id',[id])
            #colors = Variants.objects.filter(product_id=id).distinct('color_id')
            print(colors)

            colors.group_by = ['color_id'] 
            
            results = QuerySet(query=colors, model=Variants)
            #print(results)
            #raw('SELECT * FROM  product_variants  WHERE product_id=%s GROUP BY color_id',[id])
            #colors = Variants.objects.raw('SELECT * FROM  product_variants  WHERE product_id=%s GROUP BY color_id',[id])
            #colors = Variants.objects.filter(product_id=id,size_id=variants[0].size_id )
            #sizes = Variants.objects.raw('SELECT * FROM  product_variants  WHERE product_id=%s GROUP BY size_id',[id])
            sizes = Variants.objects.filter(product_id=id,color_id=variants[0].color_id )
            variant = Variants.objects.get(id=variants[0].id)
        context.update({'sizes': sizes, 'colors': colors,
                        'variant': variant,'query': query, "selected_c": c
                        })
    else:
        context.update({
            'product': product,
            'images': images,
            'selected_c': c
        })                    
    return render(request,'agents/detailed-product.html',context)

    '''
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
    })'''



def ajaxcolor(request):
    data = {}
    if request.POST.get('action') == 'post':
        color_id = request.POST.get('color')
        productid = request.POST.get('productid')
        sizes = Variants.objects.filter(product_id=productid, color_id=color_id)
        context = {
            'color_id': color_id,
            'productid': productid,
            'sizes': sizes,
        }
        data = {'rendered_table': render_to_string('agents/size_list.html', context=context)}
        return JsonResponse(data)
    return JsonResponse(data)    
    
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
'''
def addtocart(request):
    data = {}
    if request.POST.get('action') == 'post':
        product_id = request.POST.get("product_id")
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
        
        if variantid_1M is not None and variantid_1M != '':
            variant = Variants.objects.get(id=variantid_1M)
        else:
            variantid_1M = 0    
        variantid_3M = request.POST.get("variantid_3M")
        if variantid_3M is not None and variantid_3M != '':
            variant = Variants.objects.get(id=variantid_3M)
        else:
            variantid_3M = 0
        
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
        data = {'rendered_table': render_to_string('agents/cart-updated.html', context=context)}
        return JsonResponse(data)
    return JsonResponse(data)

def variant(current_username, customer, v, q, p_id):
    if v is not None and v != '':
        if q != '':
            variant = Variants.objects.get(id=v)
            u = User.objects.get(username=current_username)
            data = ShopCart()
            data.user_id = u.id
            data.customer = customer
            data.product_id = p_id
            data.variant_id = variant.id
            data.quantity = q
            data.save()
        else:
            print('q is none')
        return v
    else:
        v = 0
        return v
'''        