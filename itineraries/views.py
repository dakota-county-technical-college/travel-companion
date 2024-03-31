from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from itineraries.forms import userRegistrationForm
from django.contrib import messages  # Import messages framework

from utils import helpers
from .models import Activity

# Create your views here.
def index(request):
    return render(request, 'index.html')


def destination_search(request):
    context = {}
    if request.method == 'POST':
        destination = request.POST.get('destination')
        success, recommended_places_or_message = helpers.get_recommendation(destination)

        if not success:
            # In case of failure, recommended_places_or_message contains the error message.
            context['error'] = recommended_places_or_message
        else:
            # On success, it contains the list of places. Each place is a dictionary with detailed information.
            detailed_places = []
            for place in recommended_places_or_message:
                detailed_place = {
                    'title': place.get('title', ''),
                    'editSummary': place.get('editSummary', 'Summary not available'),
                    'name': place['name'],  # Assuming 'name' will always be present
                    'address': place.get('address', 'Address not available'),
                    'placeID': place.get('placeID', ''),
                    'photos': place.get('photos', ''),  # This might need conversion to a URL or similar
                    'openHour': place.get('openHour', 'Opening hours not available'),
                    'rating': place.get('rating', 'Rating not available'),
                    'businessStatus': place.get('business_status', 'Status not available'),
                    'location': place.get('location', ''),
                    'lat': place.get('lat', ''),
                    'lng': place.get('lng', ''),
                    'urlLink': place.get('urlLink', ''),  # Assuming this is a direct link to Google Maps or similar
                    # Include additional fields as necessary
                }
                detailed_places.append(detailed_place)
            
            context['places'] = detailed_places

    return render(request, 'test/searchresults.html', context)


def add_activity(request):
    if request.method == 'POST':
        print("In POST addactivity")
        
        # Retrieve all the form data from the POST request
        title = request.POST.get('title', '')
        editSummary = request.POST.get('editSummary', '')
        name = request.POST.get('name', '')
        address = request.POST.get('address', '')
        placeID = request.POST.get('placeID', '')
        photos = request.POST.get('photos', '')
        openHour = request.POST.get('openHour', '')
        rating = request.POST.get('rating', '')
        location = request.POST.get('location', '')
        urlLink = request.POST.get('urlLink', '')
        # Additional fields like northeast, southwest, website can be added similarly
        
        # Log retrieved data for verification (optional, remove in production)
        # print(f"Name: {name}, Address: {address}, Rating: {rating}, Location: {location}")

        # Proceed to save this data to your model
        new_activity = Activity(
            title=title,
            editSummary=editSummary,
            name=name,
            address=address,
            placeID=placeID,
            photos=photos,
            openHour=openHour,
            rating=rating,
            location=location,
            urlLink=urlLink,
            # Include other fields as needed
        )
        new_activity.save()
        # Redirect or render a response as needed

        return render(request, 'test/addactivity.html')


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