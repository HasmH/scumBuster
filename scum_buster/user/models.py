from django.db import models

class scumBag(models.Model):
    steam_id = models.CharField(max_length=50) #unique steamId 
    number_of_reports = models.IntegerField(default=0) #total number of reports 
    #display_name = models.CharField() #current display name  
    


