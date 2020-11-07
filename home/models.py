from django.db import models
from django.contrib.auth.models import User

class Past_search(models.Model):
    search_name=models.CharField(max_length=100)
    user=models.ForeignKey(User,on_delete=models.CASCADE)

    def _str__(self):
        return self.search_name
# Create your models here.
