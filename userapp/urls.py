from django.urls import path,include
from . import views

urlpatterns = [
    path("", views.index, name="Home"),
    path("register/", views.RegisterUser, name="register"),
    path("login/", views.LoginUser, name="Login"),
    path("post/",include('productapp.urls')),
    path("add-post/",views.addPost ,name="addpost"),
    path("all-post/",views.allPost ,name="allpost"),
    path("logout/", views.logout_request, name= "logout"),
]