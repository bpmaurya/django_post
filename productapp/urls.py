from django.urls import path,include
from . import views

urlpatterns = [
    path("", views.index, name="Home"),
    path("product_list/",views.ProductList,name="products")
]