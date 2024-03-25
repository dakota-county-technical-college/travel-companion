from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from itineraries.forms import userRegistrationForm
from django.http import JsonResponse
from itineraries.models import Activity
import requests, json

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

# Definition for the experiemental map embed page.
def map(request):
    return render(request, 'map.html')

# Definition for the view which loads our places API data
def loadPlaceData(request):
    # The places api url
    placesURL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

    # Our request. In the future these parameters will be accepted as part of the request from the frontend.
    data = {'location': '44.737,-93.079',
    'radius': 5000,
    'type': 'restaurant',
    'key': 'AIzaSyDTxHzXGYgKdtZAkIFvJOtJ4Q_-MwDRljc'}

    # Using the requests library to call the places api
    response = requests.get(placesURL, params=data)

    # load the results from the json reponse into a list
    locations = json.loads(response.text).get("results")
    
    print(locations[0])

    for location in locations:
        a = Activity()
        a.title = location.get("name")
        a.address = location.get("vicinity")

        a.rating = location.get("rating")

        a.lat = location.get("geometry").get("location").get('lat')
        a.lng = location.get("geometry").get("location").get('lng')

        a.save()
    

    # Return an HttpResponse object to the frontend containing the json data
    return JsonResponse(response.json())