from django.db import models

# Create your models here.


class Users(models.Model):
    username = models.CharField(max_length=200, unique=True, default='')
    password = models.CharField(max_length=300)
    department = models.CharField(max_length=300)

    def __str__(self):
        return self.username
