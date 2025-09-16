from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

TYPE = (
    ('print', 'Print/eBook'),
    ('comicbook', 'Comicbook'),
    ('audiobook', 'AudioBook'),
    ('podcast', 'Podcast'),
)



# Create your models here.
class Log(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    type = models.CharField(max_length=250, choices=TYPE,)
    status = models.CharField(max_length=250)
    notes = models.TextField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('log-detail', kwargs={'log_id': self.id})