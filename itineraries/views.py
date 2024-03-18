from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from itineraries.forms import userRegistrationForm

# Create your views here.
def hello_world(request):
    # Enter a name to replace "Hello World!" with "Hello {{NAME}}"
    return render(request, 'helloworld.html', {'name': ''})

@login_required(login_url='/admin/')
def authorized(request):
    return render(request, 'authorized.html')

def register(request):
    if request.method == 'POST':
        form = userRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('../hello')
    else:
        form = userRegistrationForm()
    return render(request, 'signup.html', {'form': form})

#Definition for the experiemental map embed page.
def map(request):
    return render(request, 'map.html')