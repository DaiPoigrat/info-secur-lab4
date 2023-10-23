from django.db import models


# Create your models here.
class AuthUserModel(models.Model):
    usr = models.CharField(unique=True, blank=False)
    hash = models.CharField(blank=False)

