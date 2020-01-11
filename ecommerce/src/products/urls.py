
from django.urls import path, re_path

from products.views import (
    ProductListView, 
    # product_list_view, 
    # ProductDetailView, 
    # product_detail_view,
    # ProductFeaturedListView,
    # ProductFeaturedDetailView,
    ProductDetailSlugView,

    )
app_name = "products"

urlpatterns = [
    # path('featured/', ProductFeaturedListView.as_view()),
    # re_path(r'^featured/(?P<pk>\d+)/$', ProductFeaturedDetailView.as_view()),
    path('', ProductListView.as_view(), name='list'),
    # path('products-fbv/', product_list_view), 
    # re_path(r'^products/(?P<pk>\d+)/$', ProductDetailView.as_view()),
    re_path(r'^(?P<slug>[\w-]+)/$', ProductDetailSlugView.as_view(), name='detail'),
    # re_path(r'^products-fbv/(?P<pk>\d+)/$', product_detail_view), 
    # path('admin/', admin.site.urls),
]
