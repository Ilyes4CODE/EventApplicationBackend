from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    profile_pic = models.ImageField(upload_to='Pfp/',default='Default_pfp.jpg')
    phone_number = models.CharField(max_length=50)
    followers = models.ManyToManyField(User, related_name='following_profiles')
    expired_token = models.CharField(max_length=50,null=True)


    def __str__(self):
        return self.user.username


class Events(models.Model):
    related_user = models.ForeignKey(User, null=True,on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=250)
    image = models.ImageField(upload_to='Event_pictures/')
    is_paid = models.BooleanField()
    price = models.FloatField(default=0.0)
    likers = models.ManyToManyField(User, related_name='Likers',null=True)
    dislikers = models.ManyToManyField(User, related_name='Dislikers',null=True)
    enrolled_users = models.ManyToManyField(User, related_name='enrolled_events', blank=True)
    enrollment_limit = models.PositiveIntegerField()

    def __str__(self):
        return self.title

    def update_price_if_unpaid(self):
        if not self.is_paid: 
            self.price = 0.0

class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Events, on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"