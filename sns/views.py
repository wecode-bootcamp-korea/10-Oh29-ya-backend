import json

from django.shortcuts import render
from django.http      import JsonResponse
from django.views     import View

from .models import Staff, Post, Hashtag, PostHashtag

class PostView(View):
    def get(self, request):
        try:
            post_list = Post.objects.select_related('staff').all()
            data_list = []
            for post in post_list:
                staff_id = post.staff_id
                staff_obj = Staff.objects.get(id=staff_id)
                center_table_list = list(PostHashtag.objects.filter(post_id=post.id).values())
                hashtag_list = []
                for obj in center_table_list:
                    hashtag_name = Hashtag.objects.get(id=obj['hashtag_id']).name
                    hashtag_list.append(hashtag_name)
                post_dic = {
                    'thumbnail_image':f'http://{post.thumbnail_image}',
                    'staff_logo':f'http://{staff_obj.logo_url}',
                    'staff_name':staff_obj.name,
                    'official_check':staff_obj.is_official,
                    'content':post.content,
                    'hashtag':hashtag_list
                }
                data_list.append(post_dic)
            return JsonResponse({'data':data_list}, status = 200)
        except  Exception as message:
            return JsonResponse({'message':message}, status = 401)
