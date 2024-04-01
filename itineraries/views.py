from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, PreferencesForm
from .models import PreferencesFormResponse

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

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('../hello')
    else:
        form = UserRegistrationForm()
    return render(request, 'auth/signup.html', {'form': form})

#Definition for the experiemental map embed page.
def map(request):
    return render(request, 'test/map.html')