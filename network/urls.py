
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('posts/', views.display_posts, name='display_posts'),

    # API routes
    # path("posts", views.addpost, name="addpost"),
    path("getposts/", views.getposts, name="getpost")
]
