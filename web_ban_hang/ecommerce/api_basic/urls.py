from django.urls import  path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns =[
    path ('item_api/', views.Item_list_view ,name='item_api'),
    path ('item_api/<int:pk>/', views.Item_details_view ,name='item_api'),
]

urlpatterns = format_suffix_patterns(urlpatterns)