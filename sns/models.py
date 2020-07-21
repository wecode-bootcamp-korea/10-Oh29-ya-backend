from django.db import models
#from account.models import User

class Staff(models.Model):
    name     = models.CharField(max_length = 100)
    logo     = models.URLField(max_length = 2000)
    official = models.BooleanField(default=False)

    class Meta:
        db_table = 'staff'

    def __str__(self):
        return self.name

class Post(models.Model):
    content       = models.TextField()
    thumbnail_img = models.URLField(max_length = 2000)
    modal_video   = models.URLField(max_length = 2000, null = True)
    staff         = models.ForeignKey(Staff, on_delete = models.CASCADE)
    #user          = models.ManyToManyField(User, through = 'PostLike')

    class Meta:
        db_table = 'posts'

    def __str__(self):
        return self.content

'''
class PostLike(models.Model):
    posts = models.ForeignKey(Post, on_delete = models.CASCADE)
    users = models.ForeignKey(User, on_delete = models.CASCADE)

    class Meta:
        db_table = 'posts_likes'
'''

class Hashtag(models.Model):
    name  = models.CharField(max_length = 50)
    posts = models.ManyToManyField(Post, through = 'PostHashtag')

    class Meta:
        db_table = 'hashtags'

    def __str__(self):
        return self.name

class PostHashtag(models.Model):
    posts    = models.ForeignKey(Post, on_delete = models.CASCADE)
    hashtags = models.ForeignKey(Hashtag, on_delete = models.CASCADE)

    class Meta():
        db_table = 'posts_hashtags'
