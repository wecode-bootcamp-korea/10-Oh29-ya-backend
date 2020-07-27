import bcrypt
import hashlib
import json
import jwt
import os
import requests
import sys

from django.http            import JsonResponse
from django.core.validators import (
    validate_email,
    RegexValidator
)
from django.core.exceptions import (
    ValidationError,
    ObjectDoesNotExist
)
from django.views           import View

from my_settings            import (
    SECRET_KEY,
    ALGORITHM
)
from .models import (
    Brand,
    Category,
    Subcategory,
    Detail,
    Product,
    Image,
    LikeProduct,
    SpecialOrder
)
from account.models import User

class CategoryView(View):
    # get메소드를 사용하고 싶지만 프론트에서 get으로 데이터 주는 방법을 몰라 임시방편으로 post 로 바꿈 
    def post(self, request):
        data   = json.loads(request.body)
        product=Product.objects
        products = product.filter(category=Category.objects.get(name=data["category"]),subcategory=Subcategory.objects.get(name=data["subcategory"]) )
        productList=[
            {
                'id'            : word.id,
                'name'          : word.name,
                'price'         : word.price,
                'discount_rate' : word.discount_rate,
                'discount_price': word.discount_price,
                'brand'         : word.brand.name,
                'image'         : [image.image for image in Image.objects.filter(product_id=word.id)],
                'like_num'      : word.like_num,
                'user_like_pressed' : (True if LikeProduct.objects.filter(user=User.objects.get(id=data['user']),product=Product.objects.get(id=word.id)).exists() else False) 
            } for word in products   
        ]    
        return JsonResponse({"data":productList} ,status=200)

class LikeView(View):
    def patch(self, request):  
        data    = json.loads(request.body)
        product = Product.objects.get(id=data["product"])
        try:
            if LikeProduct.objects.filter(user=data['user'],product=data['product']).exists():
               LikeProduct.objects.get(user=data["user"],product=data['product']).delete()
               product.like_num-=1
               product.save()
            else:
                LikeProduct(
                    product=product,
                    user=User.objects.get(id=data["user"])
                ).save()
                product.like_num+=1
                product.save()
            return JsonResponse({'like_num':product.like_num},status=200)
        except ValueError:
            return JsonResponse({'message':'WRONG_VALUE'},status=400)    
        except KeyError:
            return JsonResponse({'message':'INVALID_KEYS'},status=400)
        except ObjectDoesNotExist:
            return JsonResponse({'message':'DONT_EXIST'},status=401)

class ProductView(View):
    def post(self, request): #나중에 겟으로
        data    = json.loads(request.body)
        
        # try:
        if Product.objects.filter(id=data["product"]).exists():
            product = Product.objects.prefetch_related('image_set').select_related('category').select_related('brand').select_related('subcategory').select_related('detail').get(id=data["product"])
            product_data = {
                'id'                : product.id,
                'name'              : product.name,
                'price'             : product.price,
                'discount_rate'     : product.discount_rate,
                'discount_price'    : product.discount_price,
                'brand'             : product.brand.name,
                'brand_logo'        : product.brand.logo_url,
                'brand_desc'        : product.brand.desc,
                'category'          : product.category.name,
                'subcategory'       : product.subcategory.name,
                'detail'            : product.detail.name,
                'image'             : [image.image for image in product.image_set.all()],
                'like_num'          : product.like_num,
                'delivery_fee'      : product.delivery_fee,
                'user_like_pressed' : (True if LikeProduct.objects.filter(user=User.objects.get(id=data['user']),product=Product.objects.get(id=data['product'])).exists() else False)
            }
            return JsonResponse({'data':product_data},status=200)
        else:
            return JsonResponse({'message':'INVALID_PRODUCT_ID'},status=400)
        # except:
        #     return JsonResponse({'message':'BAD_REQUEST'},status=400)

class SpecialOrderView(View):
    def get(self, request):
        special_orders = SpecialOrder.objects.select_related('product__brand')
        productList=[
            {
                'title'         : word.title,
                'subtitle'      : word.subtitle,
                'image'         : word.image,
                'time'          : word.time,
                'name'          : word.product.name,
                'price'         : word.product.price,
                'discount_rate' : word.product.discount_rate,
                'discount_price': word.product.discount_price,
                'brand'         : word.product.brand.name,
                'like_num'      : word.product.like_num 
            } for word in special_orders   
        ]    
        return JsonResponse({"data":productList} ,status=200)
