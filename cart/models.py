from django.db      import models

from account.models import (
    User,
    Delivery
)
from product.models import Product


class UserOrder(models.Model):
    user                    = models.ForeignKey(User, on_delete=models.CASCADE)
    order_time              = models.DateTimeField(auto_now_add=True)
    delivery                = models.ForeignKey(Delivery,  on_delete=models.SET_NULL , null=True)
    order_status            = models.ForeignKey('OrderStatus',on_delete=models.SET_NULL , null=True)
    time_paid               = models.DateTimeField(null=True)
    time_canceled           = models.DateTimeField(null=True)
    time_completed          = models.DateTimeField(null=True)
    time_sent               = models.DateTimeField(null=True)
    time_delivered          = models.DateTimeField(null=True)
    total_price             = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    discount                = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    final_price             = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    is_active               = models.BooleanField(default=False)

    class Meta:
        db_table = 'users_orders'

class OrderProduct(models.Model):
    user_order      = models.ForeignKey(UserOrder, on_delete=models.CASCADE,null=True)
    product         = models.ForeignKey(Product, on_delete=models.CASCADE,null=True)
    quantity        = models.IntegerField(default=1)

    class Meta:
        db_table = 'orders_products'

class OrderStatus(models.Model):
    name = models.CharField(max_length=250)

    class Meta:
        db_table = 'order_status'
