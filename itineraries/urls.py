from django.urls import path
from . import views

#URLConf
urlpatterns = [
    path('', views.index, name='home'),
    path('searchresults/', views.destination_search, name='searchresults'),
    path('addactivity/', views.add_activity, name='addactivity'),
    path('authorized', views.authorized),
    path('register/', views.register, name='register'),
    path('map/', views.map)
]
