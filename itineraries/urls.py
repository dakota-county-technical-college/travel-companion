from django.urls import path
from . import views

#URLConf
urlpatterns = [
    path('', views.index, name='home'),
    path('hello/', views.hello_world, name='hello'),
    path('authorized', views.authorized),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('map/', views.map),
    path('itinerary/<int:itinerary_id>/', views.itinerary, name='itinerary'),
    path('trips/', views.trips, name='trips'),
    path('profile/', views.profile_view, name='profile'),
]
