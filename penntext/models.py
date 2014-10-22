from django.db import models
from django.contrib.auth.models import User

class FlatPrice(models.Model):
    name = models.CharField(max_length=128) #just the name (must, wont be shown until accept)
    contact = models.CharField(max_length=128) #the phone number (optional)
    location = models.CharField(max_length=400) #place to deposit/collect money
    email = models.CharField(max_length=128)  # email address (must, won't be shown until accept)
    title = models.CharField(max_length=128) #shown always
    userid = models.IntegerField(default=0) #needed for deleting
    timeposted = models.DateTimeField(auto_now= True) #always needed
    description = models.TextField() #always shown
    pricepaid = models.DecimalField(default = 0.0, max_digits = 10, decimal_places = 2) #price needed, shown
    costofjob = models.IntegerField(default = 0) #needed, shown
    timeofjob = models.IntegerField(default = 0) #the time needed approx
    url = models.CharField(max_length=128) #for the sake of coming to the page
    picture = models.ImageField(upload_to='Ticket') #optional
    job = models.CharField(max_length=128) #job type
    typeofpay = models.IntegerField(default = 0) #0 for fixed, 1 for per hour
    nopaymentafter = models.CharField(max_length=400)
    acceptedby = models.CharField(max_length=400) #accepted job
    completioncode = models.IntegerField(default = 0)
    def __unicode__(self):
        return self.title


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    activation_key = models.CharField(max_length=40)
    phone = models.IntegerField(default=0)
    location = models.CharField(max_length=400)
    def __unicode__(self):
        return self.user.username
