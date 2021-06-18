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