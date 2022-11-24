from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('register', views.register),
    path('login', views.login),
    path('app', views.app),
    path('app/logout', views.logout),
    path('app/categories/<str:name>', views.category),
    path('app/favorites', views.favorites),
    path('app/products/<int:id_product>', views.product),

    path('api/product/<int:id_product>', views.api_product),
    path('api/roles', views.api_roles),
    path('api/users', views.api_users),
    path('api/favorites', views.api_favorites),
    path('api/products', views.api_products),
    path('api/orders', views.api_orders),

    path('auth/change-user-details', views.auth_change_user_details),
    path('auth/change-user-password', views.auth_change_user_password)
]
