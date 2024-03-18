from django.shortcuts import render
from django.views.generic import TemplateView
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.shortcuts import redirect
from django.views import View
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView

class HomeView(TemplateView):
    template_name = 'welcome.html'
    extra_context = {'today' : datetime.today}


class SignupView(CreateView):
    form_class = UserCreationForm
    template_name = 'register.html'
    success_url = 'itineraries/hello'

    #Add logic to redirect logged in user to a page where they can view their itineraries
    # def get(self, request, *args, **kwargs):
    #     if self.request.user.is_authenticated:
    #         # return redirect('itiniraries.list')
    #         print('im in')
    #     return super().get(request, *args, **kwargs)

class LogoutInterfaceView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
        # Redirect to a specific URL after logout, you can adjust this URL as needed
        return redirect('home')
    
class LoginInterfaceView(LoginView):
    template_name = 'login.html'