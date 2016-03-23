from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, post_save
from decimal import Decimal

from carts.models import Cart
import braintree
# Create your models here.

if settings.DEBUG:
    braintree.Configuration.configure(braintree.Environment.Sandbox,
        merchant_id=settings.BRAINTREE_MERCHANT_ID,
        public_key=settings.BRAINTREE_PUBLIC,
        private_key=settings.BRAINTREE_PRIVATE)

class UserCheckout(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True)
    email = models.EmailField(unique=True)
    braintree_id = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return self.email

    @property
    def get_braintree_id(self):
        instance = self

        if not instance.braintree_id:
            result = braintree.Customer.create({
                "email": instance.email
            })

            if result.is_success:
                instance.braintree_id = result.customer.id
                instance.save()
        return instance.braintree_id

    def get_client_token(self):
        customer_id = self.get_braintree_id
        if customer_id:
            client_token = braintree.ClientToken.generate({
                "customer_id":customer_id
            })
            return client_token
        return None


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


def update_braintree_id(sender, instance, *args, **kwargs):
    if not instance.braintree_id:
        instance.get_braintree_id

post_save.connect(update_braintree_id, sender=UserCheckout)

ORDER_STATUS_CHOICES=(('created','Created'),
                      ('paid','Paid'),
                      ('shipped','Shipped'),
                      ('refunded','Refunded'),
                      )

class Order(models.Model):
    status = models.CharField(max_length=10, choices=ORDER_STATUS_CHOICES, default='created')
    user = models.ForeignKey(UserCheckout, null=True)
    cart = models.ForeignKey(Cart)
    billing_address = models.ForeignKey(UserAddress, related_name='billing_address', null=True)
    shipping_address = models.ForeignKey(UserAddress, related_name='shipping_address', null=True)
    shipping_total_price = models.DecimalField(max_digits=20, decimal_places=2, default=2.99)
    order_total = models.DecimalField(max_digits=20, decimal_places=2,)
    order_id = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return str(self.cart.id)

    def mark_completed(self, order_id=None):
        self.status = "paid"
        if order_id and not self.order_id:
            self.order_id = order_id
        self.save()


def order_pre_save(sender, instance, *args, **kwargs):
    shipping_total_price = instance.shipping_total_price
    cart_total = instance.cart.total
    order_total = Decimal(shipping_total_price) + Decimal(cart_total)
    instance.order_total = order_total


pre_save.connect(order_pre_save, sender=Order)