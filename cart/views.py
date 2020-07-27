import requests
import json
import jwt

from django.http import JsonResponse
from django.views import View

from product.models import (
    Brand,
    Category,
    Subcategory,
    Detail,
    Product,
    Image,
    LikeProduct
)
from account.models import User
from cart.models import (
    UserOrder,
    OrderProduct,
    OrderStatus
)
class AddView(View):
    def post(self,request):
        data = json.loads(request.body)
        try:
            if UserOrder.objects.filter(user_id=data['user']).exists():
                if OrderProduct.objects.filter(product=data['product'], user_order=UserOrder.objects.get(user_id=data['user'])).exists():
                    cart=OrderProduct.objects.get(product=data['product'],user_order=UserOrder.objects.get(user_id=data['user']))
                    cart.quantity+=data['quantity']
                    cart.price=data['price']
                    cart.save()
                else:
                    OrderProduct(
                        user_order  = UserOrder.objects.get(user_id=data['user']),
                        product     = Product.objects.get(id=data['product']),
                        price       = data['price'],
                        quantity    = data['quantity']
                    ).save()
            else:
                UserOrder(
                    user            = User.objects.get(id=data['user']),
                    order_status    = OrderStatus.objects.get(name='장바구니'),
                ).save()
                OrderProduct(
                    user_order      = UserOrder.objects.get(user_id=data['user']),
                    product         = Product.objects.get(id=data['product']),
                    price           = data['price'],
                    quantity        = data['quantity']
                ).save()
            return JsonResponse({'message':'SUCCESS'},status=200)
        except:
            return JsonResponse({'message':'INVALID'},status=400)

class CartView(View):
    def post(self, request):
        try:
            data    = json.loads(request.body)
            products = OrderProduct.objects.select_related('user_order__user').prefetch_related('product__image_set').select_related('product__brand').filter(user_order=UserOrder.objects.get(user=User.objects.get(id=data['user'])))
            productList=[
                {
                    'id'            : word.user_order.id,
                    'product_id'    : word.product.id,
                    'name'          : word.product.name,
                    'price'         : word.product.price,
                    'discount_rate' : word.product.discount_rate,
                    'discount_price': word.product.discount_price,
                    'brand'         : word.product.brand.name,
                    'image'         : [image.image for image in word.product.image_set.all()],
                    'like_num'      : word.product.like_num ,
                    'quantity'      : word.quantity
                } for word in products   
            ]    
            return JsonResponse({"data":productList} ,status=200)
        except :
            return JsonResponse({'message':'INVALID_VALUE'},status=400)

class DeleteView(View):
    def delete(self, request):
        data    =  json.loads(request.body)
        count   = OrderProduct.objects.filter(user_order=UserOrder.objects.get(user=User.objects.get(id=data['user']))).count()
        OrderProduct.objects.get(product=data['product'], user_order=UserOrder.objects.get(user_id=data['user'])).delete()
        if count==1:
            UserOrder.objects.get(user_id=data['user']).delete()
        return JsonResponse({'message':'SUCCESS'},status=200)
            
