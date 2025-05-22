from django.db import models
from authentication.models import Custom_UserModel
from django.apps import apps

class CategoriesModel(models.Model):
    category_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)
    category_image=models.ImageField(upload_to='category_image/',null=True,blank=True)
    parent_category=models.ForeignKey("self",null=True,blank=True,on_delete=models.CASCADE,related_name="subcategories" )

    def __str__(self):
        return self.name


class ProductModel(models.Model):
    product_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)
    description=models.TextField()
    category_id=models.ForeignKey(CategoriesModel,on_delete=models.CASCADE,related_name="products")
    product_type=models.CharField(max_length=100)
    best_product=models.BooleanField(default=False)
    trending_product=models.BooleanField(default=False)
    created_at=models.DateField(auto_now=True)

    def __str__(self):
        return self.name


class ProductCategoryModel(models.Model):
    product_id=models.ForeignKey(ProductModel,on_delete=models.CASCADE)
    category_id=models.ForeignKey(CategoriesModel,on_delete=models.CASCADE)


class ProductVariantModel(models.Model):
    variant_id=models.AutoField(primary_key=True)  
    product_id=models.ForeignKey(ProductModel,on_delete=models.CASCADE,related_name='variants')
    attribute=models.CharField(max_length=100)
    value=models.CharField(max_length=255)
    extra_price=models.DecimalField(max_digits=10,decimal_places=2)
    image1=models.ImageField(upload_to='product_image/')
    image2=models.ImageField(upload_to='product_image/')
    image3=models.ImageField(upload_to='product_image/')
    stock=models.IntegerField(null=True,blank=True)
    original_price=models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    sale_price=models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    discount_per=models.IntegerField(null=True,blank=True)
    color=models.CharField(max_length=100,null=True,blank=True)
    slug=models.CharField(max_length=255,null=True,blank=True)

    def __str__(self):
        return self.slug
    
    def save(self,*args,**kwargs):

        self.slug= (self.product_id.name+'-'+(self.color if self.color else '')).replace(' ','-')
        self.sale_price=self.original_price - (self.original_price * self.discount_per / 100)
        super().save(*args,**kwargs)


class ProductAttributeModel(models.Model):
    attribute_id=models.AutoField(primary_key=True)
    product_id=models.ForeignKey(ProductModel,on_delete=models.CASCADE,null=True,blank=True)
    variant_id=models.ForeignKey(ProductVariantModel,on_delete=models.CASCADE,null=True,blank=True)
    attribute=models.CharField(max_length=100)
    value=models.CharField(max_length=255)
    

    def __str__(self):
        return self.variant_id.slug
    


class PaymentsModel(models.Model):
    payment_id=models.AutoField(primary_key=True)
    order_id=models.ForeignKey("orderapp.OrdersModel",on_delete=models.CASCADE)
    user_id=models.ForeignKey(Custom_UserModel,on_delete=models.CASCADE)
    amount=models.DecimalField(max_digits=10,decimal_places=2)
    status=models.CharField(max_length=100)
    created_at=models.DateField(auto_now=True)
    payment_mode = models.CharField(max_length=50, choices=[('Razorpay', 'Razorpay'), ('COD', 'Cash on Delivery'), ('UPI', 'UPI')], default='Razorpay')


class ReviewsModel(models.Model):
    review_id=models.AutoField(primary_key=True)
    user_id=models.ForeignKey(Custom_UserModel,on_delete=models.CASCADE)
    product_id=models.ForeignKey(ProductModel,on_delete=models.CASCADE)
    rating=models.IntegerField(default=5,choices=[(i, str(i)) for i in range(1, 6)])
    review=models.TextField(max_length=1000)
    review_image=models.ImageField(upload_to='review_image/',null=True,blank=True)
    created_at=models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_id.username} - {self.product_id.name}"

class DigitalProductModel(models.Model):
    digital_id=models.AutoField(primary_key=True)
    product_id=models.ForeignKey(ProductModel,on_delete=models.CASCADE)
    file_url=models.CharField(max_length=2000)




