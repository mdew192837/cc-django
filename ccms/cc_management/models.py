from django.db import models

# Create your models here.
class Club(models.Model):
    name = models.CharField(max_length=100)
    # Define how it's displayed
    def __str__(self):
        return self.name