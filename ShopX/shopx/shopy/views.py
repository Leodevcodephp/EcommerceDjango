from shopy.models import Product, Customer,OrderPlaced, Cart
from django.http import request
from django.shortcuts import redirect, render
from django.views import View
from .form import CustomerProfileForm, CustomerRegistrationForm
from django.contrib import messages 
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# def home(request):
#  return render(request, 'shopy/home.html')

#pass list product 
class ProductView(View):
    def get(self,request):
        totalitem = 0
        topwears = Product.objects.filter(category = 'TW')
        botwears = Product.objects.filter(category = 'BW')
        mobiles = Product.objects.filter(category = 'M')
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user = request.user))
        return render(request, 'shopy/home.html',{
            'shirt':topwears,
            'trouses':botwears,
            'phone':mobiles,
            'totalitems':totalitem
        })
    
def search(request):
    product_obj = Product.objects.all()
    item_name = request.GET.get('item_name')
    if item_name != '' and item_name is not None:
        product_object = product_obj.filter(title__icontains=item_name)
    return render(request,'shopy/base.html',{'product_obj':product_object})

#  def detail(request,id):
#     product_object = Products.objects.get(id=id)
#     return render(request,'shop/detail.html',{'product_obj': product_object})


# def product_detail(request):
#  return render(request, 'shopy/productdetail.html')

class ProductDetailView(View):
    def  get(self, request, pk):
        totalitem = 0
        product_object =  Product.objects.get(pk=pk)
        item_already_in_cart =  False
        if request.user.is_authenticated:
            item_already_in_cart = Cart.objects.filter(Q(product=product_object.id) & Q(user = request.user)).exists()
            totalitem =  len(Cart.objects.filter(user = request.user))
        return  render(request, 'shopy/productdetail.html',{'product_obj':product_object, 'item_already':item_already_in_cart,'totalitems':totalitem})

@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('pro_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart') #

@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        #cart get data from product -> query by product
        cart = Cart.objects.filter(user=user)

        #cal price
        amount = 0.0
        shipping = 70.0
        total = 0.0
        # using lambda
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        if cart_product:
            for p in cart_product:
                allitemmount = (p.quantity * p.product.discounted_price)
                amount +=allitemmount
                total = amount + shipping
            return render(request, 'shopy/addtocart.html',{'carts':cart,'cash_of_allitem': amount ,'ship': shipping, 'total_cash' :total})
        else:
            return render(request,'shopy/emptycart.html')   

def plus_cart(request):
    if request.method == 'GET':
        pro_id = request.GET['pro_id']
        c = Cart.objects.get(Q(product=pro_id) & Q(user=request.user))
        c.quantity +=1
        c.save()
        amount = 0.0
        shipping = 70.0
        total = 0.0
        # using lambda
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            allitemmount = (p.quantity * p.product.discounted_price)
            amount +=allitemmount
            total = amount + shipping
        
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'total':total
        }
        return JsonResponse(data)

def minus_cart(request):
    if request.method == 'GET':
        pro_id = request.GET['pro_id']
        c = Cart.objects.get(Q(product=pro_id) & Q(user=request.user))
        c.quantity -=1
        c.save()
        amount = 0.0
        shipping = 70.0
        total = 0.0
        # using lambda
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            allitemmount = (p.quantity * p.product.discounted_price)
            amount +=allitemmount
            total = amount + shipping
        
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'total':total
        }

        return JsonResponse(data)

def remove_cart(request):
    if request.method == 'GET':
        pro_id = request.GET['pro_id']
        c = Cart.objects.get(Q(product=pro_id) & Q(user=request.user))
        c.quantity -=1
        c.delete()
        amount = 0.0
        shipping = 70.0
        total = 0.0
        # using lambda
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            allitemmount = (p.quantity * p.product.discounted_price)
            amount +=allitemmount
            total = amount + shipping
        
        data = {
            'amount': amount,
            'total':total
        }
        return JsonResponse(data)

def buy_now(request):
 return render(request, 'shopy/buynow.html')

def profile(request):
 return render(request, 'shopy/profile.html')

@login_required
def address(request):
    add = Customer.objects.filter(user = request.user)
    return render(request, 'shopy/address.html',{'add':add, 'active':'btn-primary'})


def mobile(request, data=None):
    if data == None:
        phone = Product.objects.filter(category ='M')
    elif data == 'Redmi' or data == 'Samsung':
        phone = Product.objects.filter(category = 'M').filter(brand = 'data')
    elif data == 'above':
        phone = Product.objects.filter(category = 'M').filter(discounted_price__gt = 1000)
    elif data == 'below':
        phone = Product.objects.filter(category = 'M').filter(discounted_price__lt = 1000)
    return render(request, 'shopy/mobile.html',{'mobi': phone})

# def customerregistration(request):
#  return render(request, 'shopy/customerregistration.html')

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'shopy/customerregistration.html', {'forms':form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations, Resgistered Success!!')
            form.save()
        return render(request, 'shopy/customerregistration.html', {'forms':form})


@login_required
def checkout(request):
    user = request.user
    cus =  Customer.objects.filter(user = user)
    cart_item = Cart.objects.filter(user = user)
    amount = 0.0
    shipping = 70.0
    total = 0.0
    # using lambda
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            allitemmount = (p.quantity * p.product.discounted_price)
            amount +=allitemmount
            total = amount + shipping

    return render(request, 'shopy/checkout.html',{ 'customer': cus,'cart_items':cart_item, 'totalmoney': total})

def payment_done(request):
    user =  request.user
    cusid = request.GET.get('cusid')
    customer = Customer.objects.get(id = cusid)
    cart = Cart.objects.filter(user = user)

    for c in cart:
        OrderPlaced(user=user, customer = customer, product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect('orders')

@login_required 
def orders(request):
    op = Customer.objects.filter(user=request.user)
    return render(request, 'shopy/ordercomplete.html',{'order_placed':op})

class ProfileView(View):
    def get(self, request ):
        form = CustomerProfileForm()
        return render(request, 'shopy/profile.html',{'form':form, 'active':'btn-primary'})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr =  request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr,name=name, locality=locality, city=city,zipcode=zipcode, state=state)
            reg.save()
            messages.success(request, 'Profile update successfully!!!')
        return render(request, 'shopy/profile.html', {'form':form, 'active':'btn-primary'})

