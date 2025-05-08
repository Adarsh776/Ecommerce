from django.shortcuts import render
from .models import ProductModel
from .models import ProductVariantModel,CategoriesModel
from django.views import View
from collections import defaultdict

# Create your views here.

class Openpage(View):
    def get(self, request, *args, **kwargs):
        products = ProductModel.objects.all()
        categories = CategoriesModel.objects.filter(parent_category=None)
        
        # Pair each product with its first variant (if any)
        product_variant_pairs = []
        for product in products:
            variant = product.variants.first()
            if variant:
                product_variant_pairs.append((product, variant))

        context = {
            'product_variants': product_variant_pairs,
            'categories': categories
        }
        return render(request, 'openpage.html', context)

class EachCategory(View):
    def get(self, request, *args, **kwargs):
        # Get all products under a specific parent or subcategory
        category_id = kwargs['id']
        parent_category=CategoriesModel.objects.filter(category_id=category_id)
        subcategories=CategoriesModel.objects.filter(parent_category__in=parent_category)
        qs = ProductModel.objects.filter(category_id=category_id).select_related('category_id').prefetch_related('variants')
        
        categorized_products = dict()
 # Use first variant
        for subcat in subcategories:
            products=ProductModel.objects.filter(category_id=subcat).prefetch_related('variants')
            for product in products:
                variant=product.variants.first()
                if variant:
                    if subcat.name not in categorized_products:
                        categorized_products[subcat.name]=[(product,variant)]
                    else:
                        categorized_products[subcat.name]=categorized_products[subcat.name]+[(product,variant)]

        # Fetch all main categories with preloaded subcategories
        categories = CategoriesModel.objects.filter(parent_category__isnull=True).prefetch_related("subcategories", "subcategories__subcategories", "subcategories__products")

        context = {
            'categorized_products': categorized_products,
            'categories': categories
        }
        return render(request, 'coreap/eachcategory.html', context)

    
class ProductDetailView(View):
    def get(self,request,*args,**kwargs):
        slug = kwargs['slug']
        product = ProductVariantModel.objects.get(slug=slug)
        context={
            'product':product
        }
        return render(request,'coreap/product_detail.html',context)


