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
from .models import *

class ProductView(View):
    # get메소드를 사용하고 싶지만 프론트에서 get으로 데이터 주는 방법을 몰라 임시방편으로 post 로 바꿈 
    def post(self, request):
        data   = json.loads(request.body)
        product=Product.objects
        products = product.filter(category=Category.objects.get(name=data["category"]),subcategory=Subcategory.objects.get(name=data["subcategory"]) )
        productList=[
            {
                'id'   : word.id,
                'name' : word.name,
                'price': word.price,
                'discount_rate': word.discount_rate,
                'discount_price': word.discount_price,
                'brand': word.brand.name,
                'image': [image.image for image in Image.objects.filter(product_id=word.id)]
            } for word in products   
        ]    
        return JsonResponse({"data":productList} ,status=200)

class LikeView(View):
    def post(self, request):
        data    = json.loads(request.body)
        product=Product.objects.get(id=data["product"])
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