from django.db.models import fields
from .models import *
#thêm thu viện suer dụng serializers
from rest_framework import serializers


"""Khai bao tuong minh class ItemSerializer
class ItemSerializers(serializers.Serializer):
    id =serializers.IntegerField(read_only =True)
    title =serializers.CharField(max_length =200,required=False, allow_blank=True)
    price =serializers.FloatField(required=False ) 
    discount_price =serializers.FloatField(required=False ) 
    description =serializers.CharField(required=False ,max_length=500)
    img_product =serializers.ImageField(required=False )
    
    def create(self,validated_data):
        return ItemSerializers.objects.create(**validated_data)
    
    def update(self,validated_data,instance):
        instance.title =validated_data.get ('title', instance.title)

        instance.price =validated_data.get('price',instance.price)

        instance.discount_price =validated_data.get('discount_price',instance.discount_price)

        instance.description =validated_data.get('description',instance.description)

        instance.img_product =validated_data.get('img_product',instance.img_product)
        instance.save()
        return instance"""
class ItemSerializers(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields =['id','title','price','discount_price','description']

        
        