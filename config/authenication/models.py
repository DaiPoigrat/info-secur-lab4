from django.db import models

# Create your models here.
class AuthUserModel(models.Model):
    usr = models.CharField()
    pwd = models.CharField()