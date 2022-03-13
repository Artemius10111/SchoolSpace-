from django import test
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test.client import RequestFactory
from users.models import User
# Create your tests here.

class UsersAccountTest(TestCase):

    def test_login_redirect(self):
        self.client.force_login(User.objects.get_or_create(
            email = "test@gmail.com",
            username = "test1",
            first_name = 'first_name_test',
            last_name = "last_name_test",
            role = 'master',
            password = '1234567TestOk'
            )[0])
        response = self.client.get('/user/login/')
        self.assertEqual(response.status_code, 302)
    # def SetUp(self):
    #     "Let's create test user to test"
    #     self.factory = RequestFactory()
    #     self.new_user = get_user_model().objects.create_user(
    #         email = self.email,
    #         username = self.username, 
    #         first_name = self.first_name,
    #         last_name = self.last_name,
    #         password = self.password,
    #         role = self.role,
    #     )
    
    # def test_1(self):
    #     user = get_user_model().objects.get(username=self.username)
    #     self.assertEqual(user.username, self.username)
