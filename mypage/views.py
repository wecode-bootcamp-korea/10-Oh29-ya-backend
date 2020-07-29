import bcrypt, hashlib, json, jwt, os, requests, sys

from django.http            import JsonResponse
from django.core.validators import (
    validate_email,
    RegexValidator
)
from django.core.exceptions import (
    ValidationError,
    ObjectDoesNotExist
)

from django.views import View
from my_settings  import (
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
        try:
            user        = request.user
            products    = LikeProduct.objects.select_related('user', 'product').filter(user_id=user.id)
            productList=[{
                'id'                 : word.product.id,
                'name'               : word.product.name,
                'price'              : word.product.price,
                'discount_rate'      : word.product.discount_rate,
                'discount_price'     : word.product.discount_price,
                'brand'              : word.product.brand.name,
                'image'              : [image.image for image in Image.objects.filter(product_id=word.product.id)],
                'like_num'           : word.product.like_num,
                'user_likes_pressed' : (True if LikeProduct.objects.filter(user_id=User.objects.get(id=user.id).id, product_id=Product.objects.get(id=word.product.id).id).exists() else False)
            } for word in products]
            return JsonResponse({"data":productList} ,status=200)
        except Exception as e:
            return JsonResponse({'message':e}, status = 200)

class HeartPostView(View):
    @login_decorator
    def get(self, request):
        try:
            user       = request.user
            user_likes = User.objects.prefetch_related('likepost_set').get(id=user.id).likepost_set.all()
            my_heart_list = [{
                'user_id'            : user.id,
                'post_id'            : post.post.id,
                'thumbnail_image'    : f'http://{post.post.thumbnail_image}',
                'staff_logo'         : f'http://{post.post.staff.logo_url}',
                'staff_name'         : post.post.staff.name,
                'official_check'     : post.post.staff.is_official,
                'content'            : post.post.content,
                'hashtag'            : [inter_obj.hashtag.name for inter_obj in post.post.posthashtag_set.all()],
                'like_num'           : post.post.like_num,
                'user_likes_pressed' : (True if LikePost.objects.filter(user_id=User.objects.get(id=user.id).id,
post_id=Post.objects.get(id=post.post.id).id).exists() else False)
            } for post in user_likes]
            return JsonResponse({'my_heart_list':my_heart_list}, status = 200)
        except Exception as e:
            return JsonResponse({'message':e}, status = 401)
