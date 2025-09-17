from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings

TYPE = (
    ('print', 'Print/eBook'),
    ('comicbook', 'Comicbook'),
    ('audiobook', 'AudioBook'),
    ('podcast', 'Podcast'),
)

STATUS = (
    ('currently reading', 'Currently reading'),
    ('ditched', 'Ditched'),
    ('complete', 'Complete')
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    location = models.CharField(max_length=100)
    birthday = models.DateField('Birthday')
    favorites = models.TextField(max_length=250)

    def __str__(self):
        return self.user.username

# Create your models here.
class Log(models.Model):
    cover = models.ImageField()
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    
    type = models.CharField(max_length=250, choices=TYPE)
    status = models.CharField(max_length=250, choices=STATUS)
    notes = models.TextField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('log-detail', kwargs={'log_id': self.id})
    
    # class Meta:
    #     ordering = ['-date'] This line makes the newest feedings appear first, no dash orders in oldest-newest
    # *********** come back here to offer "sort by date added, alphabetical, etc" options