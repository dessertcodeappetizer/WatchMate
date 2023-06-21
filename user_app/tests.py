from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class RegisterTestCase(APITestCase):
    def test_register(self):
        data = {
            "username": "steven",
            "email": "steven@example.com",
            "password": "password",
            "password2": "password"
        }
        response = self.client.post(reverse('register'), data)                                   #response will take the post request and reverse will hit the register link from the url.
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)                          #it will generate the correct response and matches it with the response generated in user_app/view.py
        
class LoginTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="kane", password="kanepassword")           #Here we have created a user having the username and password
        
    def test_login(self):
        data = {                                                                                 #Here we are testing the above user if he can able to login
            "username": "kane",
            "password": "kanepassword"
        }
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK) 
        
    def test_logout(self):
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)