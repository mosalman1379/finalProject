from django.urls import path
from products.views import download_catalog

app_name='products'

urlpatterns=[
    path('download/<int:pk>/',download_catalog,name='download')
]