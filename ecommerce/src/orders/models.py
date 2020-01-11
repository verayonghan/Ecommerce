from django.db import models
from carts.models import Cart
from ecommerce.utils import unique_order_id_generator
from django.db.models.signals import pre_save, post_save
import math
from billing.models import BillingProfile


ORDER_STATUS_CHOICES = (
	("created", "created"),
	("paid","paid"),
	("shipped", "shipped"),
	("refunded", "refunded"),
	)
class OrderManager(models.Manager):
	def new_or_get(self, billing_profile, cart_obj):
		created = False
		order_qs = self.get_queryset().filter(cart=cart_obj, billing_profile=billing_profile, active=True)
		if order_qs.count() == 1:
			order_obj = order_qs.first()
			print(f"current order is {order_obj}")
		else:
			print(f"order with cart {cart_obj} and billing profile {billing_profile.email} is being created")
			order_obj = self.model.objects.create(cart=cart_obj, billing_profile=billing_profile)	
			created = True
		return order_obj, created

class Order(models.Model):
	# pk / id : 1, 2, ... -> random unique string  #hsfd5762jidv
	order_id = models.CharField(max_length=120, blank=True)
	billing_profile = models.ForeignKey(BillingProfile, null=True, blank=True, on_delete=models.CASCADE)
	# shipping_address
	# billing_address
	cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
	status = models.CharField(max_length=120, default="created", choices=ORDER_STATUS_CHOICES)
	shipping_total = models.DecimalField(default=5.99, max_digits=100, decimal_places=2)
	total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
	active = models.BooleanField(default=True)

	objects = OrderManager()

	def __str__(self):
		return self.order_id

	def update_total(self):
		cart_total = self.cart.total
		shipping_total = self.shipping_total
		new_total = math.fsum([cart_total, shipping_total])
		self.total = format(new_total, '.2f')
		self.save()
		return new_total



# generate the order_id
def pre_save_create_order_id(sender, instance, *arg, **kwargs):
	if not instance.order_id:
		instance.order_id = unique_order_id_generator(instance)

	qs = Order.objects.filter(cart=instance.cart).exclude(billing_profile=instance.billing_profile)
	if qs.exists():
		qs.update(active=False)
		print(f"setting {qs} to be inactive")


pre_save.connect(pre_save_create_order_id, sender=Order)

# generate the total
# update total : cart change -> order change
def post_save_cart_total(sender, instance, created, *args, **kwargs):
	if not created:
		print("cart changes")
		cart_obj = instance
		cart_total = cart_obj.total
		cart_id = cart_obj.id
		qs = Order.objects.filter(cart_id=cart_id)
		if qs.count() == 1:
			order_obj = qs.first()
			order_obj.update_total()
post_save.connect(post_save_cart_total, sender=Cart)


# update total : order created
def post_save_order(sender, instance, created, *args, **kwargs):
	if created:
		print(f"order {instance.order_id} is created")
		instance.update_total() 

post_save.connect(post_save_order, sender=Order)




