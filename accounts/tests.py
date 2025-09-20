from django.test import TestCase
from django.contrib.auth.models import User
from django.shortcuts import reverse


class AccountsTest(TestCase):
    """"
    log in url,by-name / log in post / after log in check login & signup pages / after log in check 'welcome, buttons,...' /
    log out post /
    sign up url,by-name / sign up post existing user info / sign up post & check redirection to log in /
    """
    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user(
            username='Johnson',
            password='ajjfdnwieu332HHHvvdf/',
        )

    def test_login_url(self):
        response1 = self.client.get(reverse('login'))
        self.assertEqual(response1.status_code, 200)
        response2 = self.client.get('/accounts/login/')
        self.assertEqual(response2.status_code, 200)
        self.assertNotContains(response2, 'You have already logged in')
        self.assertContains(response2, 'Sign up')
        self.assertContains(response2, 'Log in')

    def test_login(self):
        response1 = self.client.post(reverse('login'), {
            'username': 'Johnson',
            'password': 'ajjfdnwieu332HHHvvdf/',
        })
        self.assertEqual(response1.status_code, 302)

        response2 = self.client.get('/accounts/login/')
        self.assertContains(response2, 'welcome Johnson')
        self.assertContains(response2, 'You have already logged in')

        response3 = self.client.get('/accounts/signup/')
        self.assertContains(response3, 'You have logged in. First log out and then sign up for another account')

        response4 = self.client.post(reverse('logout'))
        self.assertEqual(response4.status_code, 302)

    def test_signup_url(self):
        response1 = self.client.get(reverse('signup'))
        self.assertEqual(response1.status_code, 200)
        response2 = self.client.get('/accounts/signup/')
        self.assertEqual(response2.status_code, 200)
        self.assertNotContains(response2, 'You have logged in. First log out and then sign up for another account')
        self.assertContains(response2, 'form')

    def test_signup(self):
        response = self.client.post(reverse('signup'), {
            'username':'Farhad',
            'password1': 'jio56ojij0j56433::K',
            'password2': 'jio56ojij0j56433::K',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='Farhad').exists())
