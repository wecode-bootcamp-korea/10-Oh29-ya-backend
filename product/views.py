import bcrypt
import hashlib
import json
import jwt
import os
import requests
import sys

from django.http                import JsonResponse
from django.core.validators     import (
    validate_email,
    RegexValidator
)
from django.core.exceptions     import (
    ValidationError,
    ObjectDoesNotExist
)
from django.views               import View
from my_settings                import (
    SECRET_KEY,
    ALGORITHM
)
from .models                    import (
    Brand,
    Category,
    Subcategory,
    Detail,
    Product,
    Image,
    LikeProduct,
    SpecialOrder
)
from account.models             import User
from account.utils              import (
    login_decorator,
    detoken
)



class CategoryView(View):
    def get(self, request):
        try:
            data                = {}
            user                = detoken(request)
            data["category"]    = request.GET.get("category",None)
            data["subcategory"] = request.GET.get("subcategory",None)
            product             = Product.objects
            products            = product.filter(category=Category.objects.get(name=data["category"]),subcategory=Subcategory.objects.get(name=data["subcategory"]))
            productList=[
                {
                    'id'                : word.id,
                    'name'              : word.name,
                    'price'             : word.price,
                    'discount_rate'     : word.discount_rate,
                    'discount_price'    : word.discount_price,
                    'brand'             : word.brand.name,
                    'image'             : [image.image for image in Image.objects.filter(product_id = word.id)],
                    'like_num'          : word.like_num,
                    'user_like_pressed' : False
                } for word in products   
            ]
            if user:
                for  temp in productList:
                    temp['user_like_pressed'] = (True if LikeProduct.objects.filter(user = User.objects.get(id = user.id),product = Product.objects.get(id = temp['id'])).exists() else False)   
            return JsonResponse({"data":productList} , status = 200)
        except TypeError:
            return JsonResponse({'message':"TYPEERROR"}, status = 400)
        except ObjectDoesNotExist:
            return JsonResponse({'message':"DOES_NOT_EXIST"}, status = 400)

class LikeView(View):
    @login_decorator
    def patch(self, request):  
        data    = json.loads(request.body)
        user    = request.user
        product = Product.objects.get(id = data["product"])
        try:
            if LikeProduct.objects.filter(user = user.id, product = data['product']).exists():
               LikeProduct.objects.get(user = user.id, product = data['product']).delete()
               product.like_num-=1
               product.save()
            else:
                LikeProduct(
                    product = product,
                    user    = User.objects.get(id = user.id)
                ).save()
                product.like_num += 1
                product.save()
            return JsonResponse({'like_num':product.like_num}, status = 200)
        except ObjectDoesNotExist:
            return JsonResponse({'message':"DOES_NOT_EXIST"}, status = 400)
        except json.decoder.JSONDecodeError:
            return JsonResponse({'message':"JSON_ERROR"}, status = 400)
        except ValueError:
            return JsonResponse({'message':"VALUEERROR"}, status = 400)

class ProductView(View):
    def get(self, request, product_id): 
        user            = detoken(request)
        try:
            product = Product.objects.prefetch_related('image_set').select_related('category').select_related('brand').select_related('subcategory').select_related('detail').get(id=product_id)
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
                'user_like_pressed' : False
            }
            if user:
                product_data['user_like_pressed'] = (True if LikeProduct.objects.filter(user=User.objects.get(id=user.id),product=Product.objects.get(id=product_id)).exists() else False)
            return JsonResponse({'data':product_data}, status =200)
        except ObjectDoesNotExist:
            return JsonResponse({'message':"DOES_NOT_EXIST"}, status = 400)
        except json.decoder.JSONDecodeError:
            return JsonResponse({'message':"JSON_ERROR"}, status = 400)
        except ValueError:
            return JsonResponse({'message':"VALUEERROR"}, status = 400)

class SpecialOrderView(View):
    def get(self, request):
        try:
            special_orders = SpecialOrder.objects.select_related('product__brand')
            productList=[
                {
                    'id'            : word.id,
                    'title'         : word.title,
                    'subtitle'      : word.subtitle,
                    'image'         : word.image,
                    'start'         : word.time.split('~')[0].replace('.','/').rstrip(),
                    'end'           : word.time.split('~')[1].replace('.','/'),
                    'name'          : word.product.name,
                    'price'         : word.product.price,
                    'product_id'    : word.product.id,
                    'discount_rate' : word.product.discount_rate,
                    'discount_price': word.product.discount_price,
                    'brand'         : word.product.brand.name,
                    'like_num'      : word.product.like_num 
                } for word in special_orders   
            ]    
            return JsonResponse({"data":productList} , status = 200)
        except ObjectDoesNotExist:
            return JsonResponse({'message':"DOES_NOT_EXIST"}, status = 400)
        except json.decoder.JSONDecodeError:
            return JsonResponse({'message':"JSON_ERROR"}, status = 400)
        except ValueError:
            return JsonResponse({'message':"VALUEERROR"}, status = 400)
