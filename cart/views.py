import requests
import json
import jwt

from django.http    import JsonResponse
from django.views   import View

from account.utils  import (
    login_decorator,
    detoken
)

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
from cart.models    import (
    UserOrder,
    OrderProduct,
    OrderStatus
)

class AddView(View):
    @login_decorator
    def post(self,request):
        data = json.loads(request.body)
        user = detoken(request)
        try:
            if UserOrder.objects.filter(user_id = user.id).exists():
                if OrderProduct.objects.filter(product = data['product'], user_order = UserOrder.objects.get(user_id = user.id)).exists():
                    cart = OrderProduct.objects.get(product = data['product'],user_order = UserOrder.objects.get(user_id = user.id))
                    cart.quantity += data['quantity']
                    cart.save()
                    return JsonResponse({'message':'SUCCESS'},status = 200)
                else:
                    OrderProduct(
                        user_order  = UserOrder.objects.get(user_id = user.id),
                        product     = Product.objects.get(id = data['product']),
                        quantity    = data['quantity']
                    ).save()
                    return JsonResponse({'message':'SUCCESS'},status = 200)
            else:
                UserOrder(
                    user            = User.objects.get(id = user.id),
                    order_status    = OrderStatus.objects.get(name = '장바구니'),
                ).save()
                OrderProduct(
                    user_order      = UserOrder.objects.get(user_id = user.id),
                    product         = Product.objects.get(id = data['product']),
                    quantity        = data['quantity']
                ).save()
                return JsonResponse({'message':'SUCCESS'},status = 200)
        except Exception as e:
            return JsonResponse({'message': e},status = 400)

class CartView(View):
    @login_decorator
    def get(self, request):
        try:
            user     = request.user
            products = OrderProduct.objects.select_related('user_order__user').prefetch_related('product__image_set').select_related('product__brand').filter(user_order=UserOrder.objects.get(user=User.objects.get(id=user.id)))
            productList = [
                {
                    'id'            : word.product.id,
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


class UpdateView(View):
    @login_decorator
    def patch(self, request):
        try:
            data            = json.loads(request.body)
            user            = request.user
            order_product   = OrderProduct.objects.select_related('userorder__user').select_related('product')
            user_order      = UserOrder.objects.select_related('user').get(user=User.objects.get(id=user.id),order_status=OrderStatus.objects.get(name='장바구니'))
            order_product.filter(user_order = user_order).delete()
            if data['cart'][0]["product_list"] == None:
                user_order.delete()
            else :
                user_order.total_price = float(data['cart'][1]['total'].replace(',',''))
                data_list              = list(data['cart'][0].values())[0]
                for data in data_list:
                    order_product.create(user_order = user_order,product = Product.objects.get(id = data['id']),quantity = data['quantity'])
            return JsonResponse({'message':'SUCCESS'},status=200)
        except :
            return JsonResponse({'message':'INVALID_VALUE'},status=400)
class CountCartView(View):
    @login_decorator
    def get(self, request):
        try:
            user            = request.user
            order_product   = OrderProduct.objects.select_related('userorder__user').select_related('product')
            user_order      = UserOrder.objects.select_related('user').get(user = User.objects.get(id = user.id),order_status = OrderStatus.objects.get(name = '장바구니'))
            count           = order_product.filter(user_order = user_order).count()
            return JsonResponse({'count':count}, status = 200)
        except:
            return JsonResponse({'message':'INVALID_VALUE'},status=400) 

class DeleteView(View):
    @login_decorator
    def delete(self, request):
        try:
            data          = json.loads(request.body)
            user          = request.user
            order_product = OrderProduct.objects.select_related('userorder')
            count         = OrderProduct.objects.filter(user_order = UserOrder.objects.get(user = User.objects.get(id = user.id))).count()
            OrderProduct.objects.get(product = data['product'], user_order = UserOrder.objects.get(user_id = user.id)).delete()
            if count ==  1:
                UserOrder.objects.get(user_id = user.id).delete()
            return JsonResponse({'message':'SUCCESS'},status = 200)
        except:
            return JsonResponse({'message':'INVALID_VALUE'},status=400) 
            
