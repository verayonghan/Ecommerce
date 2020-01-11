from django.db import models
from django.conf import settings
from decimal import Decimal

User = settings.AUTH_USER_MODEL
from products.models import Product
from django.db.models.signals import pre_save, post_save, m2m_changed
# Create your models here.
class CartManager(models.Manager):

	def new_or_get(self, request):
		cart_id = request.session.get("cart_id", None)
		qs = self.get_queryset().filter(id=cart_id)
		if qs.count() == 1:
			new_obj = False
			print(f"cart {cart_id} exists")
			cart_obj = qs.first()
			if request.user.is_authenticated and cart_obj.user is None:
				cart_obj.user = request.user # associate with user
				cart_obj.save()
		else:
			new_obj = True
			cart_obj = self.new_cart(user=request.user)
			request.session["cart_id"] = cart_obj.id
		return cart_obj, new_obj


	def new_cart(self, user=None):
		# print(user) #vera
		user_obj = None
		if user is not None :
			if user.is_authenticated:
				user_obj = user
		print("new cart created")
		return self.model.objects.create(user=user_obj)


class Cart(models.Model):
	user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE) 
	products = models.ManyToManyField(Product, blank=True)
	subtotal = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
	total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)

	updated = models.DateTimeField(auto_now=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	objects = CartManager()

	def __str__(self):
		return str(self.id)


# caculate the total price
def m2m_changed_cart_receiver(sender, instance, action, *arg, **kwargs):
	if action == "post_add" or action == "post_remove" or action == "post_clear":	
		products = instance.products.all()
		total = 0
		for x in products:
			total += x.price
		if instance.subtotal != total:
			instance.subtotal = total
			instance.save()

m2m_changed.connect(m2m_changed_cart_receiver, sender=Cart.products.through)




def pre_save_cart_receiver(sender, instance, *arg, **kwargs):
	if instance.subtotal > 0:
		total = float(instance.subtotal)*float(1.12) # add tax
		instance.total = total
	else:
		instance.total = 0

pre_save.connect(pre_save_cart_receiver, sender=Cart)
