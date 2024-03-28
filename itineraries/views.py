from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from itineraries.forms import userRegistrationForm

# Create your views here.
def index(request):
    return render(request, 'index.html')

def destinations(request):
    return render(request, 'test/destinations.html', {'name': ''})

@login_required(login_url='admin/')
def authorized(request):
    return render(request, 'auth/authorized.html')

def register(request):
    if request.method == 'POST':
        form = userRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('../hello')
    else:
        form = userRegistrationForm()
    return render(request, 'auth/signup.html', {'form': form})

#Definition for the experiemental map embed page.
def map(request):
    return render(request, 'test/map.html')