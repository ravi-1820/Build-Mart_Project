"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from myapp import views

urlpatterns = [
   
    path('index/', views.index, name='index'),
    path('sindex/', views.sindex, name='sindex'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('fpass/', views.fpass, name='fpass'),
    path('otp/', views.otp, name='otp'),
    path('newpass/', views.newpass, name='newpass'),
    path('cpass/', views.cpass, name='cpass'),
    path('add_product/', views.add_product, name='add_product'),
    path('view_product/', views.view_product, name='view_product'),
    path('Error/', views.Error, name='Error'),
    path('bestseller/', views.bestseller, name='bestseller'),
    path('cart/', views.cart, name='cart'),
    path('cheackout/', views.cheackout, name='cheackout'),
    path('profile/', views.profile, name='profile'),
    path('shop/', views.shop, name='shop'),
    path('single/<int:pk>/', views.single, name='single'),
    path('edit_product/<int:pk>/', views.edit_product, name='edit_product'),
    path('delete/<int:pk>/', views.delete, name='delete'),
]
