from django.urls import path, re_path
from .views import SearchProductListView
    
app_name = "search"

urlpatterns = [
    path('', SearchProductListView.as_view(), name='query'),

]
