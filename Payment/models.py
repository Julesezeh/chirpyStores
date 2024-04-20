from django.db import models
import secrets
from MAIN.models import Product
from USERS.models import CustomUser

# Create your models here.


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderItem')
    total_amount = models.FloatField( default=0.0)
    is_active = models.BooleanField(default = True)
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user}"
    
    def update_total_amount(self):
        total_amount = 0.0
        for order_item in self.orderitem_set.all():
            total_amount += order_item.line_total
        self.total_amount = total_amount

    def save(self, *args, **kwargs):
        # Call the save method of the parent class to save the Order instance
        super().save(*args, **kwargs)

    def save_and_update_total_amount(self, *args, **kwargs):
        # Call update_total_amount to recalculate the total amount
        self.update_total_amount()
        # Now call the save method to persist the changes
        self.save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    line_total = models.FloatField(default = 0.0)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order #{self.order.id}"




class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    ref = models.CharField(max_length=200)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    email = models.EmailField()
    verified = models.BooleanField(default=False)
    payment_status = models.CharField(max_length=20, default='Pending')
    transaction_id = models.CharField(max_length=255, blank=True, null=True)
    payment_timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-payment_timestamp",)

    def save(self, *args,**kwargs):
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            existing_object = Payment.objects.filter(ref=ref)
            if not existing_object:
                self.ref = ref
        super().save(*args,**kwargs)

    def amount_value(self) -> int:
        return self.order.total_amount * 100

    def __str__(self):
        return f"Payment for Order #{self.order.id}"
    


