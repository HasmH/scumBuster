from django.db import models

class scumBag(models.Model):
    steamId = models.CharField(max_length=50) #unique steamId 
    numberOfReports = models.IntegerField() #total number of reports 
    trustFactor = models.BooleanField() #algorithmically computed trust factor based on number of reports and number of reports of people on its friends list 


