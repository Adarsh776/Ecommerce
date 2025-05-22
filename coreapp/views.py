from django.shortcuts import render,redirect
from django.db.models import Avg,Count
from authentication.models import Custom_UserModel
from orderapp.models import OrdersModel
from .models import ProductVariantModel,CategoriesModel,ProductAttributeModel,ReviewsModel,ProductModel
from .forms import ReviewsForm
from django.views import View
from collections import defaultdict
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


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
        reviews=ReviewsModel.objects.filter(product_id=product_id)
        total_reviews = reviews.count()
        average_rating = reviews.aggregate(avg=Avg('rating'))['avg'] or 0
        
        
        
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

        
        rating_counts = reviews.values('rating').annotate(count=Count('rating'))
        rating_dict = {str(i): 0 for i in range(5,0,-1)}
        for item in rating_counts:
            rating_dict[str(item['rating'])] = item['count']

        

        context = {
            'product': product,
            'similar_products': similar_products,
            'best_deals': best_deals,
            'recently_viewed': recent_products,
            "attributedict":attributedict,
            "color_variant_map": color_variant_map,
            'reviews': reviews,
            'total_reviews': total_reviews,
            'avg_rating': average_rating,
            'rating_counts': rating_dict
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

@method_decorator(login_required,name='dispatch')
class ProductReview(View):
    def get(self, request, *args, **kwargs):
        user_id = Custom_UserModel.objects.get(id=request.user.id)
        product_id = kwargs['id']

        product = ProductModel.objects.get(product_id=product_id)

        has_purchased = OrdersModel.objects.filter(
            user_id=user_id,
            order_items__product_id=product
        ).exists()

        reviewed = ReviewsModel.objects.filter(
            user_id=user_id,
            product_id=product
            ).first()
        
        if has_purchased and reviewed:
            form=ReviewsForm(instance=reviewed)
        else:
            form=ReviewsForm()

        context = {
            'form':form,
            'has_purchased':has_purchased
        }
        return render(request,'coreap/product_review.html',context)
    
    def post(self, request, *args, **kwargs):
        user_id = Custom_UserModel.objects.get(id=request.user.id)
        product_id = kwargs['id']
        obj=ReviewsModel.objects.filter(user_id=user_id,product_id=product_id).first()
        product = ProductModel.objects.get(product_id=product_id)
        if obj:
            form = ReviewsForm(request.POST,request.FILES,instance=obj)
        else:
            form = ReviewsForm(request.POST,request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.user_id = user_id
            review.product_id = product
            form.save()
            return redirect('productdetail',slug=product.variants.first().slug)
        return redirect('productdetail',slug=product.variants.first().slug)



class SearchResultsView(ListView):
    model = ProductModel
    template_name = 'coreap/search_results.html'
    context_object_name = 'results'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return ProductModel.objects.filter(name__icontains=query)