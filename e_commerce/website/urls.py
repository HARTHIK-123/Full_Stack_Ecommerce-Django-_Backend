from django.urls import include, path
from . import views
from .views import  dashboard, signup, login_view, users_list
urlpatterns = [
    path('',views.home, name='home'),
    path('login/',views.login, name='login'),
    path('logout/',views.logout, name='logout'),
    # path("api/products/", views.product_list),
    # path("api/products/<int:pk>/", views.product_list),  # for PUT & DELETE
    # path("api/signup/", views.signup),
    # path("api/login/", views.login_view, name="login"),
    #  path("api/users/", users_list),

    # API URLs -Don't touch when you are not with me.
     path("api/",include('website.api.urls')),
     path("users/", views.user_list_view, name="user-list"),
     path('add-user/', views.add_user_view, name='add-user'),
    #  path("website/", include("website.urls")),
    #  path("dashboard/", dashboard, name="dashboard"),
]
