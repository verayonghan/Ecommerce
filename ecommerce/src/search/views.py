from django.shortcuts import render
from products.models import Product
from django.views.generic import ListView

# Create your views here.
class SearchProductListView(ListView): 
	template_name = "search/view.html"

	def get_context_data(self, *args, **kwargs):
		context = super(SearchProductListView, self).get_context_data(*args, **kwargs)
		query = self.request.GET.get('q')
		context['query'] = query
		# SearchQuery.objects.create(query=query)
		return context

	def get_queryset(self, *args, **kwargs):
		request = self.request
		# print(request.GET)
		query = request.GET.get('q', None)
		if query is not None:
			# lookups = Q(title__icontains=query) | Q(desc__icontains=query)
			# return Product.objects.filter(title__icontains=query) 
			# return Product.objects.filter(lookups).distinct()
			return Product.objects.search(query)
		return Product.objects.featured()
		# title__icontains='Hat' : field contains this
		# title__iexact='Hat' : field is exactly this
 