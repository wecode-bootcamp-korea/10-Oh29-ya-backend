from django.db import models

from account.models import User



class Brand(models.Model):
    name                = models.CharField(max_length = 50)
    desc                = models.CharField(max_length = 300)
    logo_url            = models.URLField(max_length  = 500)
    brand_category      = models.ManyToManyField('Category',through='BrandCategory' )   
    
    class Meta:
        db_table = 'brands'

    def __str__(self):
        return self.name

class Category(models.Model):
    name                    = models.CharField(max_length = 50,unique=True)
    category_subcategory    = models.ManyToManyField('Subcategory',through='CategorySubcategory')
    
    class Meta:
        db_table            = 'categories'

    def __str__(self):
        return self.name

class Subcategory(models.Model):
    name                    = models.CharField(max_length = 50,unique=True)

    class Meta:
        db_table            = 'subcategories'

    def __str__(self):
        return self.name

class Detail(models.Model):
    name                    = models.CharField(max_length = 50)
    category_subcategory    = models.ForeignKey('CategorySubcategory',on_delete=models.SET_NULL,null=True)

    class Meta:
        db_table = 'details'

    def __str__(self):
        return self.name
    

class CategorySubcategory(models.Model):
    category        = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    subcategory     = models.ForeignKey(Subcategory, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table    = 'categories_subcategories'

class  BrandCategory(models.Model):
    brand           = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True)
    category        = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table    = 'brands_categories'
    
    




class Product(models.Model):
    name            = models.CharField(max_length = 250, unique=True)
    price           = models.DecimalField(max_digits=10, decimal_places=2)
    discount_rate   = models.IntegerField(default=0)
    discount_price  = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_fee    = models.IntegerField(default=0)
    brand           = models.ForeignKey('Brand',on_delete=models.SET_NULL,null=True)
    category        = models.ForeignKey('Category',on_delete=models.SET_NULL,null=True)
    subcategory     = models.ForeignKey('Subcategory',on_delete=models.SET_NULL,null=True)
    detail          = models.ForeignKey('Detail',on_delete=models.SET_NULL,null=True)
    like_num        = models.IntegerField(default=0)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'products'

    def __str__(self):
        return self.name

class Image(models.Model):
    image           = models.URLField(max_length=2000)
    product         = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)

    class Meta:
        db_table = 'images'

class UserOrder(models.Model):
    user                = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    order_time          = models.DateTimeField(auto_now_add=True)
    delivery_address    = models.CharField(max_length = 250)
    order_status        = models.ForeignKey('OrderStatus',on_delete=models.SET_NULL,null=True)
    time_paid           = models.DateTimeField(null=True)
    time_canceled       = models.DateTimeField(null=True)
    time_completed      = models.DateTimeField(null=True)
    time_snet           = models.DateTimeField(null=True)
    time_delivered      = models.DateTimeField(null=True)
    total_price         = models.DecimalField(max_digits=10, decimal_places=2)
    discount            = models.DecimalField(max_digits=10, decimal_places=2)
    final_price         = models.DecimalField(max_digits=10, decimal_places=2)
    active              = models.BooleanField(default=False)

    class Meta:
        db_table = 'users_orders'

class SpecialOrder(models.Model):
    text            = models.TextField()
    image           = models.URLField(max_length=2000)
    product         = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    end             = models.DateTimeField(null=True)

    class Meta:
        db_table = 'specialorders'

class OrderStatus(models.Model):
    status_name     = models.CharField(max_length=250)

    class Meta:
        db_table    = 'order_status'

class LikeProduct(models.Model):
    user            = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    product         = models.ForeignKey(Product, on_delete=models.CASCADE,null=True)

    class Meta:
        db_table    = 'like_product'