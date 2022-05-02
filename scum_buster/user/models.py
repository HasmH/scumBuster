from django.db import models

class scumBag(models.Model):
    steamId = models.CharField(max_length=50)
    numberOfReports = models.CharField(max_length=50)
    trustFactor = models.BooleanField()


