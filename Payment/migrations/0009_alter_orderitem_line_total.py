# Generated by Django 5.0.1 on 2024-04-12 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Payment', '0008_alter_order_total_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='line_total',
            field=models.FloatField(default=0.0),
        ),
    ]
