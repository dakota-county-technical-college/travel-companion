from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

class Itinerary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(blank=True)
    num_travelers = models.IntegerField(default=1)

    def __str__(self):
        return self.title
    
class Day(models.Model):
    itinerary = models.ForeignKey(Itinerary, on_delete=models.CASCADE)
    date = models.DateField()
    day_number = models.IntegerField()

    def __str__(self):
        return f"{self.itinerary.title} - Day {self.day_number}"
    
class Activity (models.Model):
    day = models.ForeignKey(Day, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    start_time = models.TimeField()
    end_time = models.TimeField()
    # Add other fields as needed
    editSummary = models.CharField(max_length=255) # summary of the place
    name = models.CharField(max_length=255) #name of place
    address = models.CharField(max_length=255) #address of place
    placeID = models.CharField(max_length=255) # unique identifier of place
    
    # add a PHOTOS field, decide where to upload the photos from API call
    
    openHour = models.CharField(max_length=255) # open hours of a business/place
    periods = models.CharField(max_length=255) # array of opening periods covering 7 days in chronological order
    ##### DECIDE IF WE WANT THIS ----> businessStatus = models.CharField(max_length=255) 
            #status of business/place -> Operational, Closed Temporarily, Closed Permanently
    
    rating = models.CharField(max_length=255) # rating of the place/business
    urlLink = models.CharField(max_length=255) # contains URL of the Official Google page for the place. 
        ##Applications must link to or embed this page on any screen 
            ##that shows detailed results about the place to the user.
    location = models.CharField(max_length=255) # location of the business/place
    lat = models.CharField(max_length=255) # lattitude in decimal degrees
    lng = models.CharField(max_length=255) # longitude in decimal dgrees
    northeast = models.CharField(max_length=255) # LatLng
    southwest = models.CharField(max_length=255) # LatLng
    website = models.CharField(max_length=255) # Authoritative website for the place, like the business homepage.

    def __str__(self):
        return self.name

class PreferencesFormResponse(models.Model):
    destination = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    travelers = models.IntegerField()

    def __str__(self):
        return f"Destination: {self.destination}, Travelers: {self.travelers}"