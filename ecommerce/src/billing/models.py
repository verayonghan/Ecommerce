from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from accounts.models import GuestEmail

# Create your modeels here.
User = settings.AUTH_USER_MODEL

# abc@gmail.com -> can have many billing profile
# user abc@gmail.com -> 1 billing profile

class BillingProfileManager(models.Manager):
	def new_or_get(self, request):
		user = request.user
		guest_email_id = request.session.get("guest_email_id")
		created = False
		obj = None
		if user.is_authenticated:
			print("logged-in user checkout")
			obj, created = self.model.objects.get_or_create(user=user, email=user.email)
		elif guest_email_id is not None: 
			print("guest user checkout")
			guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
			obj, created = self.model.objects.get_or_create(email=guest_email_obj)
		else:
			pass

		return obj, created

class BillingProfile(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	email = models.EmailField()
	active = models.BooleanField(default=True)
	update = models.DateTimeField(auto_now=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	objects = BillingProfileManager()
	# customer_id in Stripe or Braintree

	def __str__(self):
		return self.email 

# def billing_profile_created_receiver(sender, instance, created, *args, **kwargs):
# 	if created:
# 		print("Send to stripe/Braintree")
# 		instance.customer_id = newID
# 		instance.save()


# when a user is created, a billing profile is created for the user
def user_create_receiver(sender, instance, created, *args, **kwargs):
	if created:
		BillingProfile.objects.get_or_create(user=instance, email=instance.email)

post_save.connect(user_create_receiver, sender=User)