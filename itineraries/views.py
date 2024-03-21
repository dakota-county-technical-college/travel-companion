from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from itineraries.forms import userRegistrationForm
from django.http import JsonResponse
import requests

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

def loadPlaceData(request):
    placesURL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    data = {'location': {44.737, -93.079 },
    'radius': 1500,
    'type': 'restaurant',
    'key': 'AIzaSyDTxHzXGYgKdtZAkIFvJOtJ4Q_-MwDRljc'}

    response = requests.get(placesURL, params=data)
    
    print(response.text)

    return JsonResponse(response)