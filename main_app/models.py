from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import validate_comma_separated_integer_list


# Create your models here.
class userProfile(models.Model):

    user = models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username



class saveLaunch(models.Model):
    userid = models.IntegerField(blank=True)
    rocketid = models.IntegerField(blank=True,unique=True)




class launchEnt:
    def __init__(self,launch):
        self.id = launch['id']
        self.name = launch['name']
        self.locationName = launch['location']['name']
        self.locationCC = launch['location']['countryCode']
        self.locationPadLat = launch['location']['pads'][0]['latitude']
        self.locationPadLon = launch['location']['pads'][0]['longitude']
        self.windowStart = launch['windowstart']
        self.windowEnd = launch['windowend']
        self.rocketName = launch['rocket']['name']
        self.rocketImg = launch['rocket']['imageURL']
        try:
            self.missionName = launch['missions'][0]['name']
            self.missionDesc = launch['missions'][0]['description']
        except IndexError:
            self.missionName = "N/A"
            self.missionDesc = "N/A"
    def getLoc(self):
        return (self.locationPadLat,self.locationPadLon)