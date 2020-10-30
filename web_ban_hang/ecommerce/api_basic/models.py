from django.shortcuts import reverse
from django.db import models

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