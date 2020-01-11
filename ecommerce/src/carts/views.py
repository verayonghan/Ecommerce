from django.shortcuts import render,redirect

from .models import Cart
from accounts.forms import LoginForm, GuestForm
from products.models import Product
from orders.models import Order
from billing.models import BillingProfile
from accounts.models import GuestEmail
from addresses.forms import AddressForm

# Create your views here.

# def cart_create(user=None):
# 	cart_obj = Cart.objects.create(user=None)
# 	print("new cart created")
# 	return cart_obj




def cart_home(request):
	# print(request.session) # django.contrib.sessions.backends.db.SessionStore
	# print(dir(request.session))
	# print(request.session.session_key)
	# request.session.set_expiry(300) # 5min
	# request.session['first_name'] = 'Justin' # setter
	# request.session['user'] = request.user # Object of type AnonymousUser/User is not JSON serializable	
	# del request.session["cart_id"]

	cart_obj, new_obj = Cart.objects.new_or_get(request)
	# cart_id = request.session.get("cart_id", None)
	# qs = Cart.objects.filter(id=cart_id)
	# if qs.count() == 1:
	# 	print(f"cart_id {cart_id} exists")
	# 	cart_obj = qs.first()
	# 	if request.user.is_authenticated and cart_obj.user is None:
	# 		cart_obj.user = request.user # associate with user
	# 		cart_obj.save()
	# else:
	# 	cart_obj = Cart.objects.new_cart(user=request.user)
	# 	request.session["cart_id"] = cart_obj.id
	return render(request, "carts/home.html", {"cart" : cart_obj})

def cart_update(request):
	product_id = request.POST.get("product_id");
	if product_id is not None:
		try:
			product_obj = Product.objects.get(id=product_id)
		except Product.DoesNotExist:
			print("Show message to user : product is gone")
			return redirect("cart:home")

		cart_obj, new_obj = Cart.objects.new_or_get(request)
		if product_obj in cart_obj.products.all():
			cart_obj.products.remove(product_obj)
		else:
			cart_obj.products.add(product_obj) 

		request.session["cart_items"] = cart_obj.products.count()
	return redirect("cart:home")

def checkout_home(request):
	cart_obj, cart_created = Cart.objects.new_or_get(request)
	
	if cart_created or cart_obj.products.count() == 0:
		return redirect("cart:home")


	login_form = LoginForm()
	guest_form = GuestForm()
	address_form = AddressForm()
	# billing_address_form = AddressForm()



	billing_profile, biling_profile_created = BillingProfile.objects.new_or_get(request)
	# guest_email_id = request.session.get("guest_email_id")
	

	# if user.is_authenticated:
	# 	print("logged-in user checkout")
	# 	billing_profile, biling_profile_created = BillingProfile.objects.get_or_create(user=user, email=user.email)
	# elif guest_email_id is not None: 
	# 	print("guest user checkout")
	# 	guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
	# 	billing_profile, biling_guest_profile_created = BillingProfile.objects.get_or_create(email=guest_email_obj)
	# else:
	# 	pass

	order_obj = None
	if billing_profile is not None: # cart + biling_profile -> order
		order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
		# order_qs = Order.objects.filter(cart=cart_obj, billing_profile=billing_profile, active=True)
		# if order_qs.count() == 1:
		# 	order_obj = order_qs.first()
		# 	print(f"current order is {order_obj}")
		# 	order_qs.update(active=False) 
		# else:
		# 	old_order_qs = Order.objects.exclude(billing_profile=billing_profile).filter(cart=cart_obj, active=True)
		# 	if old_order_qs.exists():
		# 		old_order_qs.update(active=False)
		# 	print(f"order with cart {cart_obj} and billing profile {billing_profile.email} is being created")
		# 	order_obj = Order.objects.create(cart=cart_obj, billing_profile=billing_profile)	
		
	context = {
		"order": order_obj,
		"billing_profile": billing_profile,
		"login_form": login_form,
		"guest_form": guest_form,
		"address_form": address_form,
		# "biling_address_form": billing_address_form
	}
	return render(request, "carts/checkout.html", context)
