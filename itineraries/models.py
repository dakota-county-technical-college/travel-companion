from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

class Traveler(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, null=True, blank=True)

    def itineraries(self):
        return self.itinerary_set.all()
    
    def __str__(self):
        return self.user.username
    
    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name
    
    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name
    
    class Meta:
        ordering = ['user__first_name', 'user__last_name']


class Activity (models.Model):
    title = models.CharField(max_length=255)
    editSummary = models.CharField(max_length=255) # summary of the place
    name = models.CharField(max_length=255) #name of place
    address = models.CharField(max_length=255) #address of place
    placeID = models.CharField(max_length=255)  # unique identifier of the place
    photos = models.TextField(blank=True, null=True)  # Storing photo URLs or references
    openHour = models.CharField(max_length=255) # open hours of a business/place
    periods = models.TextField(blank=True, null=True)  # JSON string of opening periods covering 7 days
    businessStatus = models.CharField(max_length=255, blank=True, null=True)
    rating = models.CharField(max_length=255) # rating of the place/business
    urlLink = models.CharField(max_length=255, blank=True, null=True)  # URL of the Official Google page for the place.
    location = models.CharField(max_length=255) # location of the business/place
    northeast = models.CharField(max_length=255, blank=True, null=True)  # Northeast bound of the location
    southwest = models.CharField(max_length=255, blank=True, null=True)  # Southwest bound of the location
    website = models.CharField(max_length=255, blank=True, null=True)  # Authoritative website for the place

    def __str__(self):
        return self.name


########## FOLLOWING ARE MERELY PLACEHOLDERS THAT SHOULD BE REVISED AND MOVED ABOVE THIS LINE WHEN READY ##########

class Day(models.Model):
    date = models.DateField()
    activities = models.ManyToManyField(Activity, through='ActivityAssignment')

    def __str__(self):
        return self.date.strftime('%Y-%m-%d')
    
class ActivityAssignment(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    day = models.ForeignKey(Day, on_delete=models.CASCADE)
    start_time = models.TimeField()

    class Meta:
        ordering = ['start_time']
    
    def __str__(self):
        return f"{self.activity.title} on {self.day.date.strftime('%Y-%m-%d')} at {self.start_time.strftime('%H:%M')}"
    
class Itinerary(models.Model):
    traveler = models.ForeignKey(Traveler, on_delete=models.CASCADE, null=True, blank=True)
    days = models.ManyToManyField(Day)

    def __str__(self):
        if self.traveler:
            return f"Itinerary for {self.traveler.user.username}"
        else:
            return "Unassigned Itinerary"