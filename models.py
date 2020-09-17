from django.db import models
from django.core.validators import RegexValidator

class Contests(models.Model):
    contid = models.IntegerField()
    conttype = models.CharField(max_length=10)
    duration = models.IntegerField()
    phase = models.CharField(max_length=20)
    name = models.CharField(max_length=200)
    url = models.URLField()
    difficulty = models.IntegerField()

    def __str__(self):
        return self.name

class Problems(models.Model):
    contestId = models.IntegerField(null=True)
    index = models.CharField(max_length=4)	
    name = models.CharField(max_length=200)
    rating = models.IntegerField(null=True)
    userssolved = models.IntegerField(null=True)
    tags = models.TextField(null=True)
    def __str__(self):
        return self.name
    
# class Invitees(models.Model):
#     phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed and with a country code")
#     cfhandle = models.CharField(max_length=100)
#     emailid = models.EmailField(max_length=100)
#     status = models.IntegerField(null=True,blank=True)
#     mobile = models.CharField(validators=[phone_regex], max_length=17, blank=True, null=True) # validators should be a list
#     currtime = models.TimeField(auto_now=True)
#     def __str__(self):
#         return self.cfhandle

class CFUsers(models.Model):
    page_visits = models.IntegerField(default=0)
    handle = models.CharField(max_length=100)

    def __str__(self):
        return self.handle