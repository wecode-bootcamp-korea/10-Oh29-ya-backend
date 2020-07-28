from django.http      import JsonResponse
from django.views     import View

from .models import (
    Staff,
    Post,
    Hashtag,
    PostHashtag
)

class PostView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            post_list = Post.objects.select_related('staff')
            data_list = [{
                'id'              : post.id,
                'thumbnail_image' : f'http   : //{post.thumbnail_image}',
                'staff_logo'      : f'http://{post.staff.logo_url}',
                'staff_name'      : post.staff.name,
                'official_check'  : post.staff.is_official,
                'content'         : post.content,
                'hashtag'         : [post.hashtag_set.get(id=obj['hashtag_id']).name for obj in post.posthashtag_set.values()]
                } for post in post_list]
            return JsonResponse({'data':data_list}, status = 200)
        except  Exception as message:
            return JsonResponse({'message':message}, status = 401)
