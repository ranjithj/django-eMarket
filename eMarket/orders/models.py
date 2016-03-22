from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
from decimal import Decimal

from carts.models import Cart
# Create your models here.

class UserCheckout(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email

ADDRESS_TYPE = (
    ('billing', 'Billing'),
    ('shipping','Shipping'),
)

class UserAddress(models.Model):
    user = models.ForeignKey(UserCheckout)
    addr_type = models.CharField(max_length=30, choices=ADDRESS_TYPE)
    street = models.CharField(max_length=40)
    zipcode = models.PositiveIntegerField()
    state = models.CharField(max_length=40)
    city = models.CharField(max_length=40)

    def __str__(self):
        return self.street

    def get_address(self):
        return "%s, %s, %s %s" %(self.street, self.city, self.state, self.zipcode)

ORDER_STATUS_CHOICES=(('created','Created'),
                      ('completed','Completed'),
                      )

class Order(models.Model):
    status = models.CharField(max_length=10, choices=ORDER_STATUS_CHOICES, default='created')
    user = models.ForeignKey(UserCheckout, null=True)
    cart = models.ForeignKey(Cart)
    billing_address = models.ForeignKey(UserAddress, related_name='billing_address', null=True)
    shipping_address = models.ForeignKey(UserAddress, related_name='shipping_address', null=True)
    shipping_total_price = models.DecimalField(max_digits=20, decimal_places=2, default=2.99)
    order_total = models.DecimalField(max_digits=20, decimal_places=2,)

    def __str__(self):
        return str(self.cart.id)

    def mark_completed(self):
        self.status = "completed"
        self.save()


def order_pre_save(sender, instance, *args, **kwargs):
    shipping_total_price = instance.shipping_total_price
    cart_total = instance.cart.total
    order_total = Decimal(shipping_total_price) + Decimal(cart_total)
    instance.order_total = order_total


pre_save.connect(order_pre_save, sender=Order)