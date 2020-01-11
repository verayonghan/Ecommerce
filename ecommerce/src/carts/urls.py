
from django.urls import path, re_path

from carts.views import (
    cart_home,
    cart_update,
    checkout_home,
    )

app_name = "carts"

urlpatterns = [
    path('', cart_home, name='home'),
    path('update/', cart_update, name='update'),
    path('checkout/', checkout_home, name='checkout'),
    # re_path(r'^(?P<slug>[\w-]+)/$', ProductDetailSlugView.as_view(), name='detail'),
]
