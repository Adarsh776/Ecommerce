from django.shortcuts import render
from .models import ProductModel
from .models import ProductVariantModel,CategoriesModel
from django.views import View
# Create your views here.

class Openpage(View):
    def get(self,request,*args,**kwargs):
        qs=ProductVariantModel.objects.all()
        categories=CategoriesModel.objects.filter(parent_category=None)
        context={
            'products':qs,
            'categories':categories
        }
        return render(request,'openpage.html',context)

class EachCategory(View):
    def get(self,request,*args,**kwargs):
        qs=ProductModel.objects.filter(category_id=kwargs['id'])
        qs1=ProductVariantModel.objects.filter(product_id__in=qs)
        products=zip(qs,qs1)
        context={
            'products':products
        }
        return render(request,'coreap/eachcategory.html',context)
    
class ProductDetailView(View):
    def get(self,request,*args,**kwargs):
        slug = kwargs['slug']
        product = ProductVariantModel.objects.get(slug=slug)
        context={
            'product':product
        }
        return render(request,'coreap/product_detail.html',context)


