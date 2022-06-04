from django.db import models

class scumBag(models.Model):
    steam_id = models.CharField(max_length=50) #unique steamId 
    #display_name = models.CharField() #current display name  

class report(models.Model):
    #Mapping of One to Many Relationship between a report and scumbag
    scum_bag = models.ForeignKey(scumBag, on_delete=models.CASCADE)

    #Time of Report
    time_of_report = models.DateField()

    #Enum to give users a choice on what game they were offending on
    class game(models.TextChoices):
        CSGO = 'Counter Strike: Global Offensive'
        TF2 = 'Team Fortress 2'
        CSS = 'Counter Strike: Source'
        GMOD = "Gary's Mod"
        CS16 = 'Counter Strike 1.6'

    report_game = models.CharField(max_length=50, choices=game.choices)



