# Generated by Django 5.1.7 on 2025-05-05 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coreapp', '0006_productmodel_best_product_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productmodel',
            name='trending_product',
            field=models.BooleanField(default=False),
        ),
    ]
