import json

from django.shortcuts import render
from django.http      import JsonResponse
from django.views     import View

from .models import (
    Staff,
    Post,
    Hashtag,
    PostHashtag,
    LikePost
)

from account.models import User
from account.utils  import (
    login_decorator,
    detoken
)

class PostView(View):
    def get(self, request):
        try:
            user      = detoken(request)
            post_list = Post.objects.select_related('staff')

            data_list = [{
                'post_id'            : post.id,
                'thumbnail_image'    : f'http://{post.thumbnail_image}',
                'staff_logo'         : f'http://{post.staff.logo_url}',
                'staff_name'         : post.staff.name,
                'official_check'     : post.staff.is_official,
                'content'            : post.content,
                'hashtag'            : [post.hashtag_set.get(id=obj['hashtag_id']).name for obj in post.posthashtag_set.values()],
                'like_num'           : post.like_num,
                'user_likes_pressed' : False
            } for post in post_list]

            if user:
                for tmp in data_list:
                    tmp['user_likes_pressed'] = (
                        True if LikePost.objects.filter(user_id=User.objects.get(id=user.id).id,
                                                        post_id=Post.objects.get(id=tmp['post_id']).id).exists() else False
                    )
            return JsonResponse({'data':data_list}, status = 200)
        except  Exception as message:
            return JsonResponse({'message':message}, status = 401)

class LikePostView(View):
    @login_decorator
    def patch(self, request):
        data = json.loads(request.body)
        user = request.user
        post = Post.objects.get(id=data['post'])
        try:
            if LikePost.objects.filter(user_id=user.id, post_id=data['post']).exists():
                LikePost.objects.get(user_id=user.id, post_id=data['post']).delete()
                post.like_num = len(list(LikePost.objects.filter(post_id=Post.objects.get(id=post.id))))
                post.save()
                data_list = {
                    'like_num' : post.like_num,
                    'user_likes_pressed' :
                    (True if LikePost.objects.filter(user_id=User.objects.get(id=user.id).id,
                                                     post_id=Post.objects.get(id=post.id).id).exists() else False)
                }
            else:
                LikePost(
                    post_id = post.id,
                    user_id = User.objects.get(id=user.id).id
                ).save()
                post.like_num = len(list(LikePost.objects.filter(post_id=Post.objects.get(id=post.id))))
                post.save()
                data_list = {
                    'like_num' : post.like_num,
                    'user_likes_pressed' :
                    (True if LikePost.objects.filter(user_id=User.objects.get(id=user.id).id,
                                                     post_id=Post.objects.get(id=post.id).id).exists() else False)
                }
            return JsonResponse({'data':data_list}, status = 200)
        except Exception as e:
            return JsonResponse({'message':e}, status = 401)
