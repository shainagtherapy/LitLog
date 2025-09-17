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
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, unique=True) # primary_key=True    or    unique=True

    location = models.CharField(max_length=100, blank=True)
    birthday = models.DateField('Birthday', blank=True, null=True)
    favorites = models.TextField(max_length=250, blank=True)

    def __str__(self):
        return self.user.username
    
    def get_absolute_url(self):
        return reverse('profile-detail')

# Create your models here.
class Log(models.Model):
    cover = models.ImageField(blank=True, null=True)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)

    type = models.CharField(max_length=250, choices=TYPE)
    status = models.CharField(max_length=250, choices=STATUS)
    notes = models.TextField(max_length=500, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('log-detail', kwargs={'log_id': self.id})
    
    # class Meta:
    #     ordering = ['-date'] This line makes the newest feedings appear first, no dash orders in oldest-newest
    # *********** come back here to offer "sort by date added, alphabetical, etc" options