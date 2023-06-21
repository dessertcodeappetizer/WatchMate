from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from watchlist_app.api import serializers
from watchlist_app import models

class StreamPlatformTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="kane", password="kanepassword")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.stream = models.streamplatform.objects.create(name="Netflix", about="No 1 streaming platform", website="http://netflix.com") 
        
    def test_stream_platform_create(self):
        data = {                                                                    #stream platform creation by the user
            "name": "Netflix",
            "about": "#1 streaming platform",
            "website": "http://www.netflix.com"
        }
        response = self.client.post(reverse('streamplatforms-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_streamplatform_list(self):
        response = self.client.get(reverse('streamplatforms-list'))                 #getting the whole list i.e. streamplatforms-list         
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_streamplatform_ind(self):
        response = self.client.get(reverse('streamplatforms-detail', args=(self.stream.id,)))         #we are creating a streamplatform manually and trying to get the details here
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
class WatchlistTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="kane", password="kanepassword")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.stream = models.streamplatform.objects.create(name="Netflix", about="No 1 streaming platform", website="http://netflix.com")
        self.watchlist = models.watchlist.objects.create(platform=self.stream, title="Godzilla", storyline="Dinosaur movie", active=True) 
        
    def test_watchlist_create(self):
        data = {                                                                                  #watchlist creation by the created user
            "platform": self.stream,
            "title": "Godzilla",
            "storyline": "Dinosaur movie",
            "active": True
        }
        response = self.client.post(reverse('movie-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_watchlist_list(self):
        response = self.client.get(reverse('movie-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_watchlist_ind(self):
        response = self.client.get(reverse('movie-detail', args=(self.watchlist.id,)))
        self.assertEqual(models.watchlist.objects.count(), 1)                                      #matching the no of movie.
        self.assertEqual(models.watchlist.objects.get().title, 'Godzilla')                         #matching the title
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
class ReviewTestcase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="kane", password="kanepassword")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.stream = models.streamplatform.objects.create(name="Netflix", about="No 1 streaming platform", website="http://netflix.com")
        self.watchlist = models.watchlist.objects.create(platform=self.stream, title="Godzilla", storyline="Dinosaur movie", active=True) 
        self.watchlist2 = models.watchlist.objects.create(platform=self.stream, title="Godzilla", storyline="Dinosaur movie", active=True) 
        self.review = models.Review.objects.create(review_user=self.user, rating=5, description="Great movie", watchli=self.watchlist2, active=True)
        
    def test_review_create(self):
        data = {
            "review_user": self.user,
            "rating": 5,
            "description": "Great movie",
            "watchli": self.watchlist,
            "active": True
        }
        response = self.client.post(reverse('review-create', args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    # def test_review_create_unauth(self):
    #     data = {
    #         "review_user": self.user,
    #         "rating": 5,
    #         "description": "Great movie",
    #         "watchlist": self.watchlist,
    #         "active": True
    #     }
    #     self.client.force_authenticate(user=None)
    #     response = self.client.post(reverse('review-create', args=(self.watchlist.id,)), data)
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_review_update(self):
        data = {
            "review_user": self.user,
            "rating": 4,
            "description": "Great movie -updated",
            "watchli": self.watchlist,
            "active": False
        }
        response = self.client.put(reverse('review-detail', args=(self.review.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_review_list(self):
        response = self.client.get(reverse('review-list', args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_review_ind(self):
        response = self.client.get(reverse('review-detail', args=(self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_review_user(self):
        response = self.client.get('/watch/review/?username' + self.user.username)               #This is how we check by the url
        self.assertEqual(response.status_code, status.HTTP_200_OK)