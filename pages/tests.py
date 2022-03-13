from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from users.models import User

# Create your tests here.
class HomePageContentViewTest(TestCase):
    
    
    def test_name_and_role1(self):
        self.client.force_login(User.objects.get_or_create(
            email = "test@gmail.com",
            username = "test1",
            first_name = 'first_name_test',
            last_name = "last_name_test",
            role = 'master',
            password = '1234567TestOk'
            )[0])
        response = self.client.get('/home')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertContains(response, '<p class="name">test1</p>', html=True)
        self.assertContains(response, '<p class="role">master</p>', html=True)
        print("test_name_and_role1 passed")
    
    def test_name_and_role2(self):
        self.client.force_login(User.objects.get_or_create(
            email = "test@gmail.com",
            username = "test2",
            first_name = 'first_name_test',
            last_name = "last_name_test",
            role = 'teacher',
            password = '1234567TestOk'
            )[0])
        response = self.client.get('/home')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertContains(response, '<p class="name">test2</p>', html=True)
        self.assertContains(response, '<p class="role">teacher</p>', html=True)
        print("test_name_and_role2 passed")
    
    def test_name_and_role3(self):
        self.client.force_login(User.objects.get_or_create(
            email = "test@gmail.com",
            username = "test3",
            first_name = 'first_name_test',
            last_name = "last_name_test",
            role = 'parent',
            password = '1234567TestOk'
            )[0])
        response = self.client.get('/home')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertContains(response, '<p class="name">test3</p>', html=True)
        self.assertContains(response, '<p class="role">parent</p>', html=True)
        print("test_name_and_role3 passed")
    
    def test_name_and_role4(self):
        
        self.client.force_login(User.objects.get_or_create(
            email = "test@gmail.com",
            username = "test4",
            first_name = 'first_name_test',
            last_name = "last_name_test",
            role = 'student',
            password = '1234567TestOk'
            )[0])
        response = self.client.get('/home')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertContains(response, '<p class="name">test4</p>', html=True)
        self.assertContains(response, '<p class="role">student</p>', html=True)
        print("test_name_and_role4 passed")