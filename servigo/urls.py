"""
URL configuration for servigo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include
from django.contrib.auth import views as auth_views
from users import views as user_views
from core import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('trips/', views.open_trips, name='open_trips'),
    path('trip/<int:pk>/', views.trip_details, name='trip_details'),
    path('location', views.location, name='location'),
    path('register', user_views.register, name='register'),
    path('complete', views.complete, name='complete'),
    path('profile', user_views.profile, name='profile'),
    path('login', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('', include('core.urls')),
]
