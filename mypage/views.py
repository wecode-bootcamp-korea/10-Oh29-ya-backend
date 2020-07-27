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
from product.models import (
    Brand,
    Product,
    Image,
    LikeProduct
)
from account.models import User

class HeartProductView(View):
    def post(self, request):
        data    = json.loads(request.body)
        products = LikeProduct.objects.select_related('user').select_related('product').filter(user_id=data["user"])
        productList=[
            {
                'id'            : word.product.id,
                'name'          : word.product.name,
                'price'         : word.product.price,
                'discount_rate' : word.product.discount_rate,
                'discount_price': word.product.discount_price,
                'brand'         : word.product.brand.name,
                'image'         : [image.image for image in Image.objects.filter(product_id=word.product.id)],
                'like_num'      : word.product.like_num 
            } for word in products   
        ]    
        return JsonResponse({"data":productList} ,status=200)