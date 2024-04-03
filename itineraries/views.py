from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import PreferencesForm
from .models import PreferencesFormResponse
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm

def index(request):
    if request.method == 'POST':
        form = PreferencesForm(request.POST)
        if form.is_valid():
            form_response = PreferencesFormResponse(
                destination=form.cleaned_data['destination'],
                start_date=form.cleaned_data['start_date'],
                end_date=form.cleaned_data['end_date'],
                travelers=form.cleaned_data['travelers']
            )
            form_response.save()
            return redirect('hello')
    else:
        form = PreferencesForm()
    return render(request, 'index.html', {'form': form})

def hello_world(request):
    # Enter a name to replace "Hello World!" with "Hello {{NAME}}"
    try:
        form_data = PreferencesFormResponse.objects.latest('id')
    except:
        form_data = None
    return render(request, 'test/helloworld.html', {'name': '', 'form_data': form_data})

@login_required(login_url='admin/')
def authorized(request):
    return render(request, 'auth/authorized.html')


'''
Registers a new user and redirects to the home page.

When a new user submits registration information, it's saved to the database, and then the user is redirected to the home page.
'''

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'header-main.html', {'form': form})



#Definition for the experiemental map embed page.
def map(request):
    return render(request, 'test/map.html')