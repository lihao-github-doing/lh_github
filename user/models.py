from django.db import models

# Create your models here.

class TUser(models.Model):
    username = models.CharField(max_length=20, blank=True, null=True)
    password = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.IntegerField(blank=True, null=True)
    salt = models.CharField(max_length=50,default='')

    class Meta:
        db_table = 't_user'
