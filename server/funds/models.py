from django.db import models

# Create your models here.

class Funds(models.Model):
    class Meta:
        db_table = "funds"
    name = models.CharField(max_length=256)
    fundcode = models.CharField(max_length=32)
