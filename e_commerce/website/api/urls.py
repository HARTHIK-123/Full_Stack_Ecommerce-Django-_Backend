from django.urls import path
from website.api import views
from website.views import product_list, signup, login_view, users_list
urlpatterns = [
    path("products/", views.product_list),
    path("products/<int:pk>/", views.product_list),  # for PUT & DELETE
    path("signup/", views.signup),
    path("login/", views.login_view, name="login"),
     path("users/", views.users_list),
    #  path('users/', views.users_list), 
     
]
