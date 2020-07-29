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

from sns.models import (
    Staff,
    Post,
    Hashtag,
    PostHashtag,
    LikePost
)

from account.models import User
from account.utils  import login_decorator

class HeartProductView(View):
    @login_decorator
    def get(self, request):
            user        = request.user
            products    = LikeProduct.objects.select_related('user').select_related('product').filter(user_id=user)
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

class HeartPostView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            user_likes = User.objects.prefetch_related('likepost_set').get(id=data['user']).likepost_set.all()
            my_heart_list = [{
                'user_id'            : data['user'],
                'post_id'            : post.post.id,
                'thumbnail_image'    : f'http://{post.post.thumbnail_image}',
                'staff_logo'         : f'http://{post.post.staff.logo_url}',
                'staff_name'         : post.post.staff.name,
                'official_check'     : post.post.staff.is_official,
                'content'            : post.post.content,
                'hashtag'            : [inter_obj.hashtag.name for inter_obj in post.post.posthashtag_set.all()],
                'like_num'           : post.post.like_num,
                'user_likes_pressed' : (True if LikePost.objects.filter(user_id=User.objects.get(id=data['user']).id,
                                                                        post_id=Post.objects.get(id=post.post.id).id).exists() else False)
            } for post in user_likes]
            return JsonResponse({'my_heart_list':my_heart_list}, status = 200)
        except Exception as e:
            return JsonResponse({'message':e}, status = 401)
