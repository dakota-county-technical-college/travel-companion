from django.urls import path
from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.index, name='home'),
    path('hello/', views.hello_world, name='hello'),
    path('authorized', views.authorized),
    path('register/', views.register, name='register'),
    path('map/', views.map)
]
