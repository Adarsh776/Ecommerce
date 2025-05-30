# Generated by Django 5.1.7 on 2025-03-17 15:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0001_initial'),
        ('coreapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrdersModel',
            fields=[
                ('order_id', models.AutoField(primary_key=True, serialize=False)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(max_length=100)),
                ('created_at', models.DateField(auto_now=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.custom_usermodel')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItemModel',
            fields=[
                ('order_item_id', models.AutoField(primary_key=True, serialize=False)),
                ('quatity', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coreapp.productmodel')),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orderapp.ordersmodel')),
            ],
        ),
        migrations.CreateModel(
            name='ShippingModel',
            fields=[
                ('shipping_id', models.AutoField(primary_key=True, serialize=False)),
                ('address', models.TextField()),
                ('tracking_id', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=100)),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orderapp.ordersmodel')),
            ],
        ),
    ]
