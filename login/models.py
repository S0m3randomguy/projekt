from django.db import models

class Account(models.Model):
    name        = models.CharField(max_length=100)
    username    = models.CharField(max_length=100)
    email       = models.CharField(max_length=100)
    password    = models.CharField(max_length=100)
    confirm     = models.CharField(max_length=100)