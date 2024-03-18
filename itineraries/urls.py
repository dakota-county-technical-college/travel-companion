from django.urls import path
from . import views
from django.urls import path, include

urlpatterns = [
    path('hello/', views.hello_world),
    path('authorized', views.authorized),
    path('register/', views.register, name='register'),
]
