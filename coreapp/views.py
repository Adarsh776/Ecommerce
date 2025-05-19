from django.shortcuts import render
from .models import ProductModel
from .models import ProductVariantModel,CategoriesModel,ProductAttributeModel
from django.views import View
from collections import defaultdict

# Create your views here.

class Openpage(View):
    def get(self, request, *args, **kwargs):
        
        trending_products=ProductModel.objects.filter(trending_product=True).prefetch_related('variants')
        
        electronics = CategoriesModel.objects.get(name="Electronics")
        subcategories = CategoriesModel.objects.filter(parent_category=electronics)

        categories=CategoriesModel.objects.filter(parent_category=None)

        best_electronics = ProductModel.objects.filter(
            category_id__in=subcategories,
            best_product=True
        ).prefetch_related('variants') 


        context = {
            'categories': categories,
            'best_electronics':best_electronics,
            'trending_products':trending_products
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
                    if subcat not in categorized_products:
                        categorized_products[subcat]=[(product,variant)]
                    else:
                        categorized_products[subcat]=categorized_products[subcat]+[(product,variant)]

        # Fetch all main categories with preloaded subcategories
        categories = CategoriesModel.objects.filter(parent_category__isnull=True).prefetch_related("subcategories", "subcategories__subcategories", "subcategories__products")

        context = {
            'categorized_products': categorized_products,
            'categories': categories
        }
        return render(request, 'coreap/eachcategory.html', context)

    
class ProductDetailView(View):
    def get(self, request, *args, **kwargs):
        slug = kwargs['slug']
        product = ProductVariantModel.objects.select_related('product_id__category_id').filter(slug=slug).first()

        category = product.product_id.category_id
        product_id = product.product_id.product_id
        
        
        # Get all variants of this base product
        all_variants = ProductVariantModel.objects.filter(product_id=product.product_id)

        # Build color → [variant] mapping
        color_variant_map = {}
        for variant in all_variants:
            color_attr=variant.color
            if color_attr:
                color_variant_map[color_attr]=variant


        similar_products = ProductVariantModel.objects.filter(
            product_id__category_id=category
        ).exclude(product_id=product_id)[:8]

        best_deals = ProductVariantModel.objects.filter(
            product_id__category_id=category,
            product_id__best_product=True
        ).exclude(product_id=product_id)[:8]

        # ---- RECENTLY VIEWED HANDLING ----
        recently_viewed = request.session.get('recently_viewed', [])

        if slug in recently_viewed:
            recently_viewed.remove(slug)  # move it to the front
        recently_viewed.insert(0, slug)  # add current product to front

        if len(recently_viewed) > 8:
            recently_viewed = recently_viewed[:8]

        request.session['recently_viewed'] = recently_viewed
        request.session.modified = True  # save session

        # ---- FETCH RECENT PRODUCTS ----
        recent_products = ProductVariantModel.objects.filter(slug__in=recently_viewed).exclude(slug=slug)
        recent_products = sorted(recent_products, key=lambda x: recently_viewed.index(x.slug))

        current_attributes = ProductAttributeModel.objects.filter(product_id=product_id, variant_id=product)
        attributedict = {}
        for attr in current_attributes:
            attributedict.setdefault(attr.attribute, []).append(attr.value)
        

        context = {
            'product': product,
            'similar_products': similar_products,
            'best_deals': best_deals,
            'recently_viewed': recent_products,
            "attributedict":attributedict,
            "color_variant_map": color_variant_map,
        }
        return render(request, 'coreap/product_detail.html', context)

class SubCategoryProducts(View):
    def get(self, request, *args, **kwargs):
        subcategory_id = kwargs['id']  # e.g., TV’s ID
        subcategory = CategoriesModel.objects.get(category_id=subcategory_id)

        # Get products directly under this subcategory
        products = ProductModel.objects.filter(category_id=subcategory).prefetch_related('variants')

        context = {
            'subcategory': subcategory,
            'products': products,
        }
        return render(request, 'coreap/subcategory_products.html', context)