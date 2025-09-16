from django.db import models
from django.urls import reverse

# Create your models here.
class Log(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    type = models.CharField(max_length=250)
    status = models.CharField(max_length=250)
    notes = models.TextField(max_length=500)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('log-detail', kwargs={'log_id': self.id})