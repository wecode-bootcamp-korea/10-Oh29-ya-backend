from django.db import models

class User(models.Model):
    email           = models.EmailField(max_length = 100, null = True, blank = True)
    password        = models.CharField(max_length = 100, null = True, blank = True)
    created_at      = models.DateTimeField(auto_now_add = True)
    updated_at      = models.DateTimeField(auto_now = True)
    is_active       = models.BooleanField(default = False)
    class Meta:
        db_table = 'users'
        