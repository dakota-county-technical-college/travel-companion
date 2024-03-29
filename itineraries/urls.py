from django.urls import path
from . import views

#URLConf
urlpatterns = [
    path('', views.index, name='home'),
    path('searchresults/', views.destination_search, name='searchresults'),
    path('authorized', views.authorized),
    path('register/', views.register, name='register'),
    path('map/', views.map)
]
