from django.urls import path
from .views import (
    HomeView,
    CheckoutView,
    ItemDetailView,
    add_to_cart,
    remove_from_cart,
    ProfileView,
    LoginView,
    Signup,
    CartView,
    LogoutView,
    ShopView,
    remove_single_item_from_cart,
    Categoryproductdetails,
    SearchView,
)

urlpatterns=[
    path('',HomeView,name='home'),
    path('checkout',CheckoutView.as_view(),name='checkout'),
    path('productdetail/<slug>/',ItemDetailView,name='productdetail'),
    path('add_to_cart/<slug>/',add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<slug>/',remove_from_cart,name='remove_from_cart'),
    path('profile',ProfileView,name='profile'),
    path('login',LoginView,name='login'),
    path('sign',Signup, name='signup'),
    path('cart',CartView.as_view(),name= 'cart'),
    path('logout',LogoutView,name ='logout'), 
    path('shop',ShopView,name ='shop'),
    path('remove_single_item_from_cart/<slug>/',remove_single_item_from_cart,name='remove_single_item_from_cart'),
    path('Categoryproductdetails/<slug>/',Categoryproductdetails,name ='Categoryproductdetails'),
    path('SearchView',SearchView,name ='SearchView'),
]