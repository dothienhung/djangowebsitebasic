import django
from django.core.checks import messages


#them thu vien phân trang
from django.shortcuts import redirect, render ,get_object_or_404
from django.views.generic.base import View
from .models import *
from django.views.generic import ListView,DetailView,View
from django.utils import timezone
#them method login required bat dang nhap vao tac vu can
#import q để tạo queryset tim kiem
from django.db.models import Q
#them thu vien auth 
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate,login,logout
from django.core.exceptions import *
from .forms import Checkoutform
from math import ceil
# Create your views here.

def HomeView(request):
    item_list = Item.objects.all()
    print(item_list)
    nitem =len(item_list)
    nSlides = nitem//3 +ceil((nitem/3)-(nitem//3))
    cat_list = Category.objects.all()
    slide_list =Item.objects.all()[:3]
    nslider =len(slide_list)
    context ={'item_list':item_list,'cat_list':cat_list,
              'slide_list':slide_list,'range':range(1,nSlides),
              'nSlides':nSlides,'ranges':range(1,nslider)}
    return render(request,template_name='techhome/index.html',context=context)
    
    
def ItemDetailView(request,slug):
    item_list = Item.objects.all()
    cat_list = Category.objects.all()
    item_id  = Item.objects.get(slug =slug)
    context ={'item_list':item_list,'cat_list':cat_list,'item_id' :item_id}
    return render(request,template_name='techhome/productdetails.html',context=context)
    
    
def ShopView(request):
    item_list = Item.objects.all()
    cat_list = Category.objects.all()
    context ={'item_list':item_list,'cat_list':cat_list}
    return render(request,template_name='techhome/shop.html',context=context)
    
def Categoryproductdetails(request,slug):
    category =None
    item_list = Item.objects.all()
    cat_list = Category.objects.all()
    if slug :
        category =get_object_or_404(Category,slug =slug)
        item_list =item_list.filter(item_category =category)
    
    context ={'item_list':item_list,'cat_list':cat_list,'category':category}
    return render(request,template_name='techhome/categorydetails.html',context=context)
 
def add_to_cart(request ,slug):
    if request.user.is_authenticated:
        item =get_object_or_404(Item, slug=slug)
        order_item,created =OrderItem.objects.get_or_create(item =item,user =request.user ,ordered =False)
        order_qs =Order.objects.filter(user =request.user , ordered =False)
        if order_qs.exists():
            order =order_qs[0]
            if order.items.filter(item__slug =item.slug).exists():
                order_item.quantity += 1
                order_item.save()
                return redirect("techshop:cart")
            else:
                order.items.add(order_item)
                return redirect("techshop:cart")
        else:
            ordered_date = timezone.now()
            order =Order.objects.create(user =request.user , ordered_date =ordered_date)
            order.items.add(order_item)
        return redirect("techshop:cart")
    else:
        return redirect("techshop:login")

def add_more_quantity(request,slug):
    if request.user.is_authenticated:
        pass
    

def remove_from_cart(request,slug):
    if request.user.is_authenticated:
        item =get_object_or_404(Item, slug=slug)   
        order_qs =Order.objects.filter(user =request.user , ordered =False)
        if order_qs.exists():
            order =order_qs[0]
            if order.items.filter(item__slug =item.slug).exists():
                order_item =OrderItem.objects.filter(
                    item =item,
                    user =request.user,
                    ordered =False,
                )[0]
                order.items.remove(order_item)
                return redirect("techshop:cart")
            else:
                return redirect("techshop:cart")
        else:
            return redirect("techshop:cart")
    else:
        return redirect("techshop:login")


class CartView(View):
    def get(self,*args, **kwargs):
        
        try :
            order =Order.objects.get(user =self.request.user,ordered = False)
            context ={'order':order}
            return render(self.request,template_name='techhome/cart.html',context=context) 
        except ObjectDoesNotExist:
            messages.error(self.request,"You dont have item in order")
            return redirect('techshop:productdetail')#
        
def remove_single_item_from_cart(request, slug):
    if request.user.is_authenticated:
        item = get_object_or_404(Item, slug=slug)
        order_qs = Order.objects.filter(
            user=request.user,
            ordered=False
        )
        if order_qs.exists():
            order = order_qs[0]
            # check if the order item is in the order
            if order.items.filter(item__slug=item.slug).exists():
                order_item = OrderItem.objects.filter(
                    item=item,
                    user=request.user,
                    ordered=False
                )[0]
                if order_item.quantity > 1:
                    order_item.quantity -= 1
                    order_item.save()
                else:
                    order.items.remove(order_item)
                return redirect("techshop:cart")
            else:
                messages.info(request, "This item was not in your cart")
                return redirect("techshop:productdetail", slug=slug)
        else:
            messages.info(request, "You do not have an active order")
            return redirect("techshop:productdetail", slug=slug)       
    else:
        return redirect("techshop:login")

def SearchView(request):
    """
    docstring
    """
    template ='techhome/search.html'
    item_list = Item.objects.all()
    cat_list = Category.objects.all()
    query = request.GET.get('q')
    items = Item.objects.filter(title__icontains =query)
    #phân trang tìm kiếm
    context ={
        'items':items,
        'item_list':item_list,
        'cat_list' :cat_list,
    }
    return render(request,template,context=context)

def ProfileView(request):
    
    context ={}
    return render(request,template_name ='techhome/productdetails.html')

class CheckoutView(View):
    def get(self,*args,**kwargs):
        form = Checkoutform()
        context={'form':form}
        return render(self.request,template_name='techhome/checkout.html',context=context)
    
    def post(self,*args,**kwargs):
        form =Checkoutform(self.request.POST or None)
        try :
            order =Order.objects.get(user =self.request.user,ordered = False)
            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                apartment_address= form.cleaned_data.get('apartment_address')
                country= form.cleaned_data.get('country')
                zip= form.cleaned_data.get('zip')
                #address_type = forms.cleaned_data.get('address_type')
                #same_billing_address =forms.cleaned_data.get('same_billing_address')
                #save_info =forms.cleaned_data.get('save_info')
                #payment_option=forms.cleaned_data.get('payment_option')
                billing_address = BillingAddress(
                user =self.request.user,
                street_address = street_address,
                apartment_address =apartment_address,
                country =country,
                zip =zip,   
            )
                billing_address.save()
                order.billing_address = billing_address
                order.save()
                return redirect('techshop:checkout')
            else:
                messages.Warning(self.request," Failed check out")
                return redirect('techshop:checkout')
        except ObjectDoesNotExist:
            messages.error(self.request,"You dont have item in order")
            return redirect('techshop:cart')#
       

def LoginView(request):
    if request.method =='POST':
        username =request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username =username,password =password)
        if user:
            login(request ,user)
            success_login = "User is login sucess"
            return redirect('techshop:home')
        else :
            
            return render(request,template_name='techhome/Signin.html')
    else:
        return render(request,template_name='techhome/Signin.html')

def LogoutView(request):
    if User.is_authenticated:
        logout(request)
        return redirect('techshop:login')

def Signup(request):
    if request.method =='POST':
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            user = User.objects.create_user(first_name =first_name,last_name=last_name,username = username,email=email,password=password1)
            user.save()
            return redirect('techshop:login')
        else:
            return render(request,template_name='techhome/Register.html') 
    else:
        return render(request,template_name='techhome/Register.html')
    
    
    
    