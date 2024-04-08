from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import PreferencesForm
from .models import PreferencesFormResponse
from .forms import UserRegistrationForm
from utils import helpers
from .models import Activity

def index(request):
    context = {}
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
            
            destination = form.cleaned_data['destination']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            success, recommended_places_or_message = helpers.get_recommendation(destination, start_date, end_date)
            # print(recommended_places_or_message)
            if not success:
            # In case of failure, recommended_places_or_message contains the error message.
                context['error'] = recommended_places_or_message
            else:
                # If successful, pass the structured itinerary to the context
                context['itinerary'] = recommended_places_or_message
                context['start_date'] = start_date
                context['end_date'] = end_date

        return render(request, 'test/searchresults.html', context)
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


"""
Registers a new user and redirects to the home page.
When a new user submits registration information, it's saved to the database, and then the user is redirected to the home page.
"""


def signup(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'home', {'form': form})


"""
Logs in a user and redirects to the home page.
When a user submits login credentials, it checks if the provided username and password are valid. If they are, the user is logged in and redirected to the home page.
"""


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return redirect('home')
    return render(request, 'home.html')


def logout_view(request):
    logout(request)
    return redirect('home')


# Definition for the experiemental map embed page.
def map(request):
    return render(request, 'test/map.html')

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
