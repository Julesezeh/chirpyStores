# Generated by Django 5.0.1 on 2024-05-01 23:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MAIN', '0002_shoebrand_product_out_of_stock_product_sizes_and_more'),
    ]

    operations = [
        # migrations.RemoveField(
        #     model_name='product',
        #     name='category',
        # ),

        # migrations.AddField(
        #     model_name='product',
        #     name='category',
        #     field=models.ManyToManyField(to='MAIN.productcategory'),
        # ),
        migrations.AlterField(
            model_name='product',
            name='brand',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='MAIN.shoebrand'),
        ),
    ]
