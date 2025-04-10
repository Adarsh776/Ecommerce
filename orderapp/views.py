from django.shortcuts import render,redirect
from .models import OrderItemModel,OrdersModel
from coreapp.models import ProductVariantModel,ProductModel
from authentication.models import Custom_UserModel
from django.http import HttpResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.

from authentication.models import Custom_UserModel

class AddToCartView(View):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        custom_user = Custom_UserModel.objects.get(id=request.user.id)

        product_slug = kwargs['slug']
        productvariant = ProductVariantModel.objects.get(slug=product_slug)
        product = ProductModel.objects.get(product_id=productvariant.product_id.product_id)

        orderitem = OrderItemModel.objects.create(
            product_id=product,
            price=productvariant.sale_price,
            quantity=1
        )

        total = orderitem.quantity * orderitem.price

        OrdersModel.objects.create(
            order_item=orderitem,
            total=total,
            status='not place',
            user_id=custom_user
        )

        return HttpResponse('Product added to cart successfully')



class CartView(View):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):

        try:
            custom_user = Custom_UserModel.objects.get(id=request.user.id)
        except Custom_UserModel.DoesNotExist:
            messages.error(request,"You are logged in, but not registered as a valid customer.")
            return redirect('dashboard')
        
        order = OrdersModel.objects.filter(user_id=custom_user, status='not place').first()
        if order:
            order_items = OrderItemModel.objects.filter(order_item_id=order.order_item.order_item_id)
            context = {
                'order_items': order_items,
                'order': order
            }
            return render(request, 'orderapp/cart.html', context)
        else:
            return HttpResponse('No items in the cart')