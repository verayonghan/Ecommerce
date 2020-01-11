from django.db import models
from django.db.models import Q

import random
import os

from ecommerce.utils import unique_slug_generator 
from django.db.models.signals import pre_save, post_save
from django.urls import reverse



# Create your models here.
def get_filename_ext(filepath):
	base_name = os.path.basename(filepath)
	name, ext = os.path.splitext(base_name)
	return name, ext


def upload_image_path(instance, filename):
	print(instance)
	print(filename)
	new_filename = random.randint(1, 1000000000000)
	name, ext = get_filename_ext(filename)
	final_filename = f'{new_filename}{ext}' #.format(new_filename=new_filename, ext=ext)
	return f'products/{new_filename}/{final_filename}'

class ProductQuerySet(models.query.QuerySet):
	def active(self):
		return self.filter(active=True)

	def featured(self):
		return self.filter(featured=True, active=True)

	def search(self, query):
		lookups =  (Q(title__icontains=query) |
		 			Q(desc__icontains=query) |
		  			Q(price__icontains=query) |
		  			Q(tag__title__icontains=query))
		# Q(tag__name__icontains==query)
		# tags : tshirt, t-shirt, t shirt
		return self.filter(lookups).distinct()

class ProductManager(models.Manager):

	# override 
	def get_queryset(self):
		return ProductQuerySet(self.model, using=self._db)

	def all(self):
		return self.get_queryset().active()

	def featured(self): # Product.objects.featured()
		return self.get_queryset().filter(featured=True)

	def get_by_id(self, id):
		qs = self.get_queryset().filter(id=id)
		if qs.count() == 1:
			return qs.first()
		return None

	def search(self, query):
		# lookups = Q(title__icontains=query) | Q(desc__icontains=query)
		# return self.get_queryset().active().filter(lookups).distinct()
		return self.get_queryset().active().search(query)

class Product(models.Model): 
	title = models.CharField(max_length=120)
	slug = models.SlugField(blank=True, unique=True)
	desc = models.TextField() 
	price = models.DecimalField(decimal_places=2, max_digits=20, default=39.99)
	image = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
	featured = models.BooleanField(default=False)
	active = models.BooleanField(default=True)
	timestamp = models.DateTimeField(auto_now_add=True)


	objects = ProductManager()

	def get_absolute_url(self):
		# return f'{self.slug}/'
		return reverse("products:detail", kwargs={"slug": self.slug})

	def __str__(self): # python 3
		return self.title 

	def __unicode__(self): # python 2
		return self.title 

	@property
	def name(self):
		return self.title
	

def product_pre_sava_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = unique_slug_generator(instance)

pre_save.connect(product_pre_sava_receiver, sender=Product)

