from django.http      import JsonResponse
from django.views     import View

from .models import (
    Staff,
    Post,
    Hashtag,
    PostHashtag
)

class PostView(View):
    def get(self, request):
        try:
            post_list = Post.objects.select_related('staff')
            data_list = []
            for post in post_list:
                staff_id          = post.staff_id
                staff_obj         = post.staff
                center_table_list = post.posthashtag_set.values()
                hashtag_list      = [post.hashtag_set.get(id=obj['hashtag_id']).name for obj in center_table_list]
                post_dic = {
                    'id'              : post.id,
                    'thumbnail_image' : f'http   : //{post.thumbnail_image}',
                    'staff_logo'      : f'http://{staff_obj.logo_url}',
                    'staff_name'      : staff_obj.name,
                    'official_check'  : staff_obj.is_official,
                    'content'         : post.content,
                    'hashtag'         : hashtag_list
                }
                data_list.append(post_dic)
            return JsonResponse({'data':data_list}, status = 200)
        except  Exception as message:
            return JsonResponse({'message':message}, status = 401)
