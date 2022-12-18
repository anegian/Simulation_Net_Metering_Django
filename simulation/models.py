from django.db import models

# Create your models here.
class CustomerModel(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=50)

    def __str__(self):
        return self.last_name + ' | ' + self.first_name

class PlaceModel(models.Model):
    city_name = models.CharField(max_length=50)
    district_name = models.CharField(max_length=50)
    TK = models.IntegerField()





