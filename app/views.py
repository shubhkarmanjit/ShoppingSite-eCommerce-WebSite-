from django.shortcuts import render,redirect
from django.views import View
from .models import Product,OrderPlaced,Customer,Cart
from .forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
#def home(request):
 #return render(request, 'app/home.html')

class ProductView(View):
 def get(self,request):
  totalitem=0
  mobiles=Product.objects.filter(category="M")
  topwears=Product.objects.filter(category="TW")
  bottomwears=Product.objects.filter(category="BW")
  laptops=Product.objects.filter(category="L")
  if request.user.is_authenticated:
    totalitem=len(Cart.objects.filter(user=request.user))
  return render(request,'app/home.html',{
   'mobiles':mobiles,'topwears':topwears,'bottomwears':bottomwears,'laptops':laptops, 
  'totalitem':totalitem})


class productdetailview(View):
    
    def get(self,request,pk):
        totalitem=0
        product=Product.objects.get(pk=pk)
        item_already_in_cart=False
        if request.user.is_authenticated:
          item_already_in_cart=Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        if request.user.is_authenticated:
          totalitem=len(Cart.objects.filter(user=request.user))
        return render(request,'app/productdetail.html',
        {'product':product,'item_already_in_cart':item_already_in_cart,'totalitem':totalitem})


@login_required
def add_to_cart(request):
 totalitem=0
 user=request.user
 product_id=request.GET.get('prod_id')
 product=Product.objects.get(id=product_id)
 Cart(user=user,product=product).save()
 if request.user.is_authenticated:
    totalitem=len(Cart.objects.filter(user=request.user))
 return redirect('/cart')


@login_required
def Show_Cart(request):
  totalitem=0
  if request.user.is_authenticated:
    totalitem=len(Cart.objects.filter(user=request.user))
    user=request.user
    cart=Cart.objects.filter(user=user)
    amount=0.0
    shipping_amount=40.0
    total_amount=0.0
    cart_product=[p for p in Cart.objects.all() if p.user ==user] 
    
    if cart_product:
      for p in cart_product:
        tempamount=(p.quantity*p.product.discounted_price)
        amount+=tempamount
        totalamount=amount+shipping_amount
      return render(request, 'app/addtocart.html',{'carts':cart,'totalamount':totalamount,
                                  'amount':amount,'totalitem':totalitem})
    else:
      return render(request,'app/emptycart.html',{'totalitem':totalitem})

def plus_cart(request):
  if request.method=='GET':
    prod_id=request.GET['prod_id']
     
    c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.quantity+=1
    c.save()
    amount=0.0
    shipping_amount=40.0
    cart_product=[p for p in Cart.objects.all() if p.user==request.user]
    for p in cart_product:
      tempamount=(p.quantity * p.product.discounted_price)
      amount+=tempamount
     
    data={
      'quantity':c.quantity,
      'amount':amount,
      'totalamount':amount+shipping_amount
      }
    return JsonResponse(data)
  

def minus_cart(request):
  if request.method=='GET':
    prod_id=request.GET['prod_id']
     
    c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.quantity-=1
    c.save()
    amount=0.0
    shipping_amount=40.0
    cart_product=[p for p in Cart.objects.all() if p.user==request.user]
    for p in cart_product:
      tempamount=(p.quantity * p.product.discounted_price)
      amount+=tempamount
       
    data={
      'quantity':c.quantity,
      'amount':amount,
      'totalamount':amount+shipping_amount
      }
    return JsonResponse(data)


def remove_cart(request):
  if request.method=='GET':
    prod_id=request.GET['prod_id']
    if request.user.is_authenticated:
      c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
      c.delete()
      amount=0.0
      shipping_amount=40.0
      cart_product=[p for p in Cart.objects.all() if p.user==request.user]
      for p in cart_product:
        tempamount=(p.quantity * p.product.discounted_price)
        amount+=tempamount
      
    
      data={
       
        'amount':amount,
        'totalamount':amount+shipping_amount
        }
    return JsonResponse(data)



def buy_now(request):
  
 return render(request, 'app/buynow.html')

@login_required
def address(request):
 totalitem=0
 add=Customer.objects.filter(user=request.user)
 if request.user.is_authenticated:
    totalitem=len(Cart.objects.filter(user=request.user))
 return render(request, 'app/address.html',{'add':add,'active':'btn-primary','totalitem':totalitem})



@login_required
def orders(request):
 totalitem=0
 op=OrderPlaced.objects.filter(user=request.user)
 #oq=Cart.objects.filter()
 if request.user.is_authenticated:
    totalitem=len(Cart.objects.filter(user=request.user))
 return render(request, 'app/orders.html',{'order_placed':op,'totalitem':totalitem})

def change_password(request):
 return render(request, 'app/changepassword.html')

def mobile(request,data=None):
    totalitem=0
    if data == None:
      mobiles=Product.objects.filter(category='M')
    elif data=='Redmi' or data=='Samsung'or data=='Apple' :
      mobiles=Product.objects.filter(category='M').filter(brand=data)

    elif data=='below':
      mobiles=Product.objects.filter(category='M').filter(discounted_price__lt=20000)
    
    elif data=='above':
      mobiles=Product.objects.filter(category='M').filter(discounted_price__gt=20000)

    if request.user.is_authenticated:
      totalitem=len(Cart.objects.filter(user=request.user))
    return render(request, 'app/mobile.html',{'mobiles':mobiles,'totalitem':totalitem})

def laptop(request,data=None):
    totalitem=0
    if data == None:
      laptops=Product.objects.filter(category='L')
    elif data=='Lenovo' or data=='Dell'or data=='HP' :
      laptops=Product.objects.filter(category='L').filter(brand=data)

    elif data=='Above':
      laptops=Product.objects.filter(category='L').filter(discounted_price__gt=50000)
    
    elif data=='Below':
      laptops=Product.objects.filter(category='L').filter(discounted_price__lt=50000)
    if request.user.is_authenticated:
      totalitem=len(Cart.objects.filter(user=request.user))
    return render(request, 'app/laptop.html',{'laptops':laptops,'totalitem':totalitem})

 
def topwear(request,data=None):
  totalitem=0
  if data ==None:
    topwears=Product.objects.filter(category='TW')

  elif data=='Men' or data=='Women' or data=='Kids':
    topwears=Product.objects.filter(category='TW').filter(brand=data)
  if request.user.is_authenticated:
    totalitem=len(Cart.objects.filter(user=request.user))
  return render(request, 'app/topwear.html',{'topwears':topwears,'totalitem':totalitem})

 


def bottomwear(request,data=None):
  totalitem=0
  if data==None:
    bottomwears=Product.objects.filter(category='BW')
  
  elif data=='Men' or data=='Women':
    bottomwears=Product.objects.filter(category='BW').filter(brand=data)
  if request.user.is_authenticated:
    totalitem=len(Cart.objects.filter(user=request.user))
  return render(request, 'app/bottomwear.html',{'bottomwears':bottomwears,'totalitem':totalitem})


#def login(request):
 #return render(request, 'app/login.html')

#def customerregistration(request):
 #return render(request, 'app/customerregistration.html')

class CustomerRegistrationView(View):
  
  def get(self,request):
    form=CustomerRegistrationForm()
    return render(request,'app/customerregistration.html',{'form':form})
  def post(self,request):
    form=CustomerRegistrationForm(request.POST)
    if form.is_valid():
      messages.success(request,'Congratulations! Registered Successfully')
      form.save()
     
    return render(request,'app/customerregistration.html',{'form':form})
 

@login_required
def checkout(request):
  totalitem=0
  user=request.user
  add=Customer.objects.filter(user=user)
  cart_items=Cart.objects.filter(user=user)
  amount=0.0
  shipping_amount=40.0
  totalamount=0.0
  cart_product=[p for p in Cart.objects.all() if p.user==request.user]
  if cart_product: 
    for p in cart_product:
      tempamout=(p.quantity * p.product.discounted_price)
      amount=tempamout
    totalamount=amount+shipping_amount
  if request.user.is_authenticated:
    totalitem=len(Cart.objects.filter(user=request.user))
    return render(request, 'app/checkout.html',{'add':add,
          'totalamount':totalamount,'cart_items':cart_items,'totalitem':totalitem})
  

#buy now code

 


@login_required

def payment_done(request):
  user=request.user
  custid=request.GET.get('custid')
  customer=Customer.objects.get(id=custid)
  cart=Cart.objects.filter(user=user)
  for c in cart:
    OrderPlaced(user=user,customer=customer,
      product=c.product,quantity=c.quantity).save()
    c.delete()
  return redirect('orders')

@method_decorator(login_required,name='dispatch')
class ProfileView(View):
  totalitem=0
  def get(self,request):
    form=CustomerProfileForm()
    if request.user.is_authenticated:
      totalitem=len(Cart.objects.filter(user=request.user))
    return render(request,'app/profile.html',
    {'form':form,'active':'btn-primary','totalitem':totalitem})
    

  def post(self,request):
            form=CustomerProfileForm(request.POST)
            if form.is_valid():
                usr=request.user
                name=form.cleaned_data['name']
                locality=form.cleaned_data['locality']
                city=form.cleaned_data['city']
                state=form.cleaned_data['state']
                zipcode=form.cleaned_data['zipcode']
                reg=Customer(user=usr,name=name,locality=locality,
                             city=city,state=state,zipcode=zipcode)
                reg.save()
                messages.success(request,'Congratulations !! Profile Updated Successfully')
            return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})    
    
    
