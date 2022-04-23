from django.db import models

class TrustFactor(models.Model):
    player_id = models.CharField(max_length=50)
    number_of_reports = models.CharField(max_length=50)
    trust_factor = models.BooleanField()
