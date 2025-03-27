from django.shortcuts import render
from .models import OrderItemModel,OrdersModel
from coreapp.models import ProductVariantModel,ProductModel
from authentication.models import Custom_UserModel
from django.http import HttpResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
# Create your views here.

class AddToCartView(View):
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        username=request.user
        product_slug=kwargs['slug']
        productvariant=ProductVariantModel.objects.get(slug=product_slug)
        product=ProductModel.objects.create(product_id=productvariant.product_id.product_id)
        orderitem=OrderItemModel.objects.create(product_id=product,price=productvariant.saleprice,quantity=1)
        total=orderitem.quatity*orderitem.price
        OrdersModel.objects.create(order_item=orderitem,total=total,status='not place',user_id=Custom_UserModel)
        return HttpResponse('product added to cart successfully')