from django.db import models

from account.models import User

class Staff(models.Model):
    name        = models.CharField(max_length=100)
    logo_url    = models.URLField(max_length=2000)
    is_official = models.BooleanField(default=False)

    class Meta:
        db_table = 'staff'

    def __str__(self):
        return self.name

class Post(models.Model):
    thumbnail_image = models.URLField(max_length=2000)
    content         = models.TextField()
    modal_video     = models.URLField(max_length=2000, null=True)
    staff           = models.ForeignKey(Staff, on_delete=models.CASCADE)
    like_num        = models.IntegerField(default=0)
    like            = models.ManyToManyField(User, through='LikePost')

    class Meta:
        db_table = 'posts'

    def __str__(self):
        return self.content

class Hashtag(models.Model):
    name  = models.CharField(max_length=50)
    post  = models.ManyToManyField(Post, through='PostHashtag')

    class Meta:
        db_table = 'hashtags'

    def __str__(self):
        return self.name

class PostHashtag(models.Model):
    post    = models.ForeignKey(Post, on_delete=models.CASCADE)
    hashtag = models.ForeignKey(Hashtag, on_delete=models.CASCADE)

    class Meta():
        db_table = 'posts_hashtags'

    def __str__(self):
        return self.post.id

class LikePost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)

    class Meta():
        db_table = 'likes_posts'
