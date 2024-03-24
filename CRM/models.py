from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Person(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    bio = models.CharField(max_length=50)
    birth_date = models.DateField()
    phone = models.CharField(max_length=12)
    gender = models.CharField(max_length=10)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "Person"




        


