from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
# Create your models here.

class streamplatform(models.Model):
    name = models.CharField(max_length=50)
    about = models.CharField(max_length=400)
    website = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class watchlist(models.Model):
    title = models.CharField(max_length=50)
    storyline = models.CharField(max_length=400)
    active = models.BooleanField(default=True)        #If the movie us is released for that we are setting to True
    created = models.DateTimeField(auto_now_add=True) #Its storing the time of the entity created
    platform = models.ForeignKey(streamplatform, on_delete=models.CASCADE, related_name="watchlist")    #we are making one to many relationships here. We want to show all the movies in watchlist. 
    avg_rating = models.FloatField(default=0)
    number_rating = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title
    
class Review(models.Model):
    review_user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.CharField(max_length=200)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    watchli = models.ForeignKey(watchlist, on_delete=models.CASCADE, related_name="reviews")
    
    def __str__(self):
        return str(self.rating) + "⭐ " + str(self.watchli.title) + " | " + str(self.review_user)