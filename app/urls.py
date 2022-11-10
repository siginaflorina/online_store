from django.urls import path
from . import views


from .views import About_usTemplateView
from .views import ContactTemplateView


urlpatterns = [
    path('', views.HomeTemplateView.as_view(), name='homepage'),
    path('about-us', About_usTemplateView.as_view(), name='about-us'),
    path('contact', views.ContactTemplateView.as_view(), name='contact'),
    path('register', views.register),
    path('login', views.login),
    path('app', views.app),
    path('home', views.home),

    path('roles', views.roles),
    path('users', views.users)
]

