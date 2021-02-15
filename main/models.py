from django.db import models


# Create your models here.
class RandomNumber(models.Model):
    number = models.IntegerField()


class State(models.Model):
    state = models.CharField(max_length=32)


class Token(models.Model):
    token = models.CharField(max_length=32)
