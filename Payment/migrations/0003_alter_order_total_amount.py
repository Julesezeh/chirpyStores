# Generated by Django 5.0.1 on 2024-04-01 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Payment', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='total_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10),
        ),
    ]
