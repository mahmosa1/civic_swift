from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class YourTestCase(TestCase):

    def test_signup_employee_view(self):
        response = self.client.get(reverse('signup_employee'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signupEmployee.html')

    def test_signup_employee_form_valid(self):
        data = {
            'username': 'test_employee',
            'password1': 'test_password',
            'password2': 'test_password',
        }
        response = self.client.post(reverse('signup_employee'), data)
        self.assertEqual(response.status_code, 302)  # Redirects to homepage
        # self.assertTrue(User.objects.filter(username='test_employee').exists())

    def test_signup_employee_redirect(self):
        data = {
            'username': 'test_employee',
            'password1': 'test_password',
            'password2': 'test_password',
        }
        response = self.client.post(reverse('signup_employee'), data)

    def test_signup_resident_view(self):
        response = self.client.get(reverse('signup_resident'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signupresident.html')

    def test_signup_resident_form_valid(self):
        data = {
            'username': 'test_resident',
            'password1': 'test_password',
            'password2': 'test_password',
        }
        response = self.client.post(reverse('signup_resident'), data)
        self.assertEqual(response.status_code, 302)  # Redirects to homepage
        # self.assertTrue(User.objects.filter(username='test_resident').exists())

    def test_signup_resident_form_invalid(self):
        data = {
            'username': '',  # Missing required field
            'password1': 'test_password',
            'password2': 'test_password',
        }
        response = self.client.post(reverse('signup_resident'), data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'username', 'This field is required.')

    def test_login_employee_view_get(self):
        response = self.client.get(reverse('login_employee'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'loginEmployee.html')

    def setUp(self):
        self.user = User.objects.create_user(username='test_employee', password='test_password')

    def test_login_employee_valid_credentials(self):
        data = {
            'username': 'test_employee',
            'password': 'test_password',
        }

        response = self.client.post(reverse('login_employee'), data)
        self.assertEqual(response.status_code, 302)  # Redirects to homepage
        self.assertTrue(self.client.session['_auth_user_id'])

    def test_login_employee_invalid_credentials(self):
        data = {
            'username': 'invalid_username',
            'password': 'invalid_password',
        }
        response = self.client.post(reverse('login_employee'), data)
        self.assertEqual(response.status_code, 302)  # Redirects to login_employee
        self.assertRedirects(response, reverse('login_employee'))

    def setUp(self):
        self.user = User.objects.create_user(username='test_resident', password='test_password')

    def test_login_resident_valid_credentials(self):
        data = {
            'username': 'test_resident',
            'password': 'test_password',
        }
        response = self.client.post(reverse('login_resident'), data)
        self.assertEqual(response.status_code, 302)  # Redirects to homepage
        self.assertTrue(self.client.session['_auth_user_id'])

    def test_login_resident_invalid_credentials(self):
        data = {
            'username': 'invalid_username',
            'password': 'invalid_password',
        }
        response = self.client.post(reverse('login_resident'), data)
        self.assertEqual(response.status_code, 302)  # Redirects to login_resident
        self.assertRedirects(response, reverse('login_resident'))

    def test_login_resident_redirect(self):
        data = {
            'username': 'test_resident',
            'password': 'test_password',
        }
        response = self.client.post(reverse('login_resident'), data)
        self.assertRedirects(response, reverse('homepage'))
