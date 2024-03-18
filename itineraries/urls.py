from django.urls import path
from . import views

#URLConf
urlpatterns = [
    path('hello/', views.hello_world),
    path('authorized', views.authorized),
    path('register/', views.register, name='register'),
    path('map/', views.map)
]
