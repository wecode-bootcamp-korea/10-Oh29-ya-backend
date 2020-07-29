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

class PostView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            post_list = Post.objects.select_related('staff')
            data_list = [{
                'id'              : post.id,
                'thumbnail_image' : f'http://{post.thumbnail_image}',
                'staff_logo'      : f'http://{post.staff.logo_url}',
                'staff_name'      : post.staff.name,
                'official_check'  : post.staff.is_official,
                'content'         : post.content,
                'hashtag'         : [post.hashtag_set.get(id=obj['hashtag_id']).name for obj in post.posthashtag_set.values()]
                } for post in post_list]
            return JsonResponse({'data':data_list}, status = 200)
        except  Exception as message:
            return JsonResponse({'message':message}, status = 401)

class LikePostView(View):
    def patch(self, request):
        data = json.loads(request.body)
        post = Post.objects.get(id=data['post'])
        try:
            if LikePost.objects.filter(user=data['user'], post=data['post']).exists():
                LikePost.objects.get(user_id=data['user'], post_id=data['post']).delete()
                post.like_num = len(list(LikePost.objects.filter(post_id=Post.objects.get(id=post.id))))
                post.save()
            else:
                LikePost(
                    post_id = post.id,
                    user_id = User.objects.get(id=data['user']).id
                ).save()
                post.like_num = len(list(LikePost.objects.filter(post_id=Post.objects.get(id=post.id))))
                post.save()
            return JsonResponse({'like_num':post.like_num}, status = 200)
        except Exception as e:
            return JsonResponse({'message':e}, status = 401)
