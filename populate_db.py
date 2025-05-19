import os
import django
import requests
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecommmerce.settings")  # Replace with your project name
django.setup()

from coreapp.models import ProductModel, CategoriesModel

FAKE_STORE_API = "https://fakestoreapi.com/products"

def download_image(image_url):
    try:
        img_temp = NamedTemporaryFile(delete=True)
        response = requests.get(image_url)
        img_temp.write(response.content)
        img_temp.flush()
        return File(img_temp, name=image_url.split("/")[-1])
    except Exception as e:
        print(f"Error downloading image: {e}")
        return None

def populate_products():
    response = requests.get(FAKE_STORE_API)
    data = response.json()

    for i, item in enumerate(data):
        category_name = item['category'].capitalize()

        # Create or get category
        category, created = CategoriesModel.objects.get_or_create(
            name=category_name,
            defaults={'category_image': None}
        )

        # Create Product
        product = ProductModel.objects.create(
            name=item['title'][:100],
            description=item['description'],
            category_id=category,
            product_type="physical",
            best_product=(i % 4 == 0),
            trending_product=(i % 3 == 0),
        )

        # Download and assign images (optional if using ProductVariantModel)
        from coreapp.models import ProductVariantModel

        image_file = download_image(item['image'])
        if image_file:
            ProductVariantModel.objects.create(
                product_id=product,
                attribute="default",
                value="default",
                extra_price=0.00,
                image1=image_file,
                image2=image_file,
                image3=image_file,
                stock=10,
                original_price=float(item['price']) + 10,
                sale_price=float(item['price']),
                discount_per=10,
                color="default",
            )

        print(f"✅ Added: {product.name}")

if __name__ == "__main__":
    populate_products()
