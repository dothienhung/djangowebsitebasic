#import reverse tra ve duong dan co id
from django.shortcuts import reverse
from django.db import models
#import thu vien setting su dun user he thong
from django.conf import settings
from django_countries.fields import CountryField
# Create your models here.

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)
ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)

class Category(models.Model):
    cat_title = models.CharField(blank=True ,null =True,max_length=100)
    slug = models.SlugField()
    def __str__(self):
        return self.cat_title
    
    def getidcategoryURL(self):
        return reverse("techshop:Categoryproductdetails",kwargs={
            'slug' : self.slug
        })
    

class Item(models.Model):
    pass
    title = models.CharField(max_length =200,null =True ,blank=True)
    price = models.FloatField(null=True ,blank =True) 
    discount_price = models.FloatField(null=True ,blank =True) 
    description =models.TextField(null=True,blank=True,max_length=500)
    item_category =models.ForeignKey(Category,null =True,on_delete =models.CASCADE)
    label = models.CharField(choices=LABEL_CHOICES, max_length=2,null=True)
    slug = models.SlugField()
    img_product =models.ImageField(null =True,blank=True)
    def __str__(self):
        return self.title
    
    @property
    def imageURL(self):
	    try:
		    url = self.img_product.url
	    except:
		    url = ''
	    return url
    
    def get_absolute_url(self):
        return reverse("techshop:productdetail",kwargs={
            'slug' :self.slug
        })
    
    def get_product_to_cart(self):
        return reverse("techshop:add_to_cart",kwargs={
            'slug' :self.slug
        })
    
    def delete_product_to_cart(self):
        return reverse("techshop:remove_from_cart",kwargs={
            'slug' :self.slug
        })


    


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    item = models.ForeignKey(Item,on_delete=models.CASCADE)
    quantity=models.IntegerField(null=True,default=1)
    ordered = models.BooleanField(default =False) 

    def __str__(self):
        return self.item.title 
   
    def total_one_product(self):
        return self.item.discount_price*self.quantity
   
    def total_product(self):
        return self.item.price*self.quantity
    
    def total_save(self):
        return self.total_product()-self.total_one_product()
    @property
    def total_all_item(self):
        if self.item.discount_price:
            return self.total_one_product
        return self.total_product

class Order(models.Model):
    pass
    #cai dat user dua vao user model setting
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date= models.DateTimeField(auto_now_add=True,null=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default =False)
    billing_address = models.ForeignKey('BillingAddress',on_delete =models.SET_NULL,null =True)

    def __str__(self):
        return self.user.username
    
    
    def total(self):
        total =0
        for order_item in self.items.all():
            total += order_item.total_all_item()
        return str(total)
    
class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)

    def __str__(self):
        return self.user.username
