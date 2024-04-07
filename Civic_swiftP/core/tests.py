from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

class AccessTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Creating a test user and superuser
        cls.user = get_user_model().objects.create_user(username='testuser', email='user@example.com', password='testpass123')
        cls.admin_user = get_user_model().objects.create_superuser('admin', 'admin@example.com', 'testpass123')

    def test_homepage_access(self):
        """Homepage is accessible without login."""
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)

    def test_signup_resident_view_access(self):
        """Signup page for residents is accessible without login."""
        response = self.client.get(reverse('signup_resident'))
        self.assertEqual(response.status_code, 200)

    def test_signup_employee_view_access(self):
        """Signup page for employees is accessible without login."""
        response = self.client.get(reverse('signupEmployee'))
        self.assertEqual(response.status_code, 200)

    def test_login_employee_page_access(self):
        """Login page for employees is accessible without login."""
        response = self.client.get(reverse('loginEmployee'))
        self.assertEqual(response.status_code, 200)

    def test_login_resident_page_access(self):
        """Login page for residents is accessible without login."""
        response = self.client.get(reverse('loginResident'))
        self.assertEqual(response.status_code, 200)

    def test_logout_redirects_to_homepage(self):
        """Logout should redirect to the homepage."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('homepage'))

    def test_volunteer_page_access(self):
        """Volunteer page is accessible without login."""
        response = self.client.get(reverse('Volunteer'))
        self.assertEqual(response.status_code, 200)

    def test_new_post_page_access_after_login(self):
        """New post page should be accessible after login."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('new-post'))
        self.assertEqual(response.status_code, 200)

    def test_create_message_page_access_after_login(self):
        """Create message page should be accessible after login."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('create-message'))
        self.assertEqual(response.status_code, 200)

    def test_report_problem_page_access_after_login(self):
        """Report problem page should be accessible after login."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('report_problem'))
        self.assertEqual(response.status_code, 200)

    def test_view_problem_reports_page_access_after_login(self):
        """Problem reports page should be accessible after login."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('problem_reports'))
        self.assertEqual(response.status_code, 200)

    def test_upload_file_page_access_after_login(self):
        """Upload file page should be accessible after login."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('upload_file'))
        self.assertEqual(response.status_code, 200)


    def test_successful_login_redirects_to_correct_page(self):
        """
        After successful login, the user is redirected to the expected page.
        """
        login_response = self.client.post(reverse('loginEmployee'), {'username': 'testuser', 'password': 'testpass123'})
        # Assuming the login view redirects to 'homepage' after successful login
        self.assertRedirects(login_response, reverse('EmployeeM'))


    def test_logout_clears_session(self):
        """
        Logging out clears the session and redirects to the homepage.
        """
        self.client.login(username='testuser', password='testpass123')
        session_key_before = self.client.session.session_key
        self.client.get(reverse('logout'))
        session_key_after = self.client.session.session_key
        self.assertNotEqual(session_key_before, session_key_after)
        self.assertRedirects(self.client.get(reverse('logout')), reverse('homepage'))

    def test_successful_login_redirects_to_correct_page2(self):
        """
        After successful login, the user is redirected to the expected page.
        """
        login_response = self.client.post(reverse('loginResident'), {'username': 'testuser', 'password': 'testpass123'})
        # Assuming the login view redirects to 'homepage' after successful login
        self.assertRedirects(login_response, reverse('ResidentM'))

    def test_logout_clears_session(self):
        """
        Logging out clears the session and redirects to the homepage.
        """
        self.client.login(username='testuser', password='testpass123')
        session_key_before = self.client.session.session_key
        self.client.get(reverse('logout'))
        session_key_after = self.client.session.session_key
        self.assertNotEqual(session_key_before, session_key_after)
        self.assertRedirects(self.client.get(reverse('logout')), reverse('homepage'))

    # Additional tests...

    def test_access_static_pages(self):
        """
        Static pages are accessible without authentication.
        """
        pages = [reverse('homepage'), reverse('signup_resident'), reverse('signupEmployee'), reverse('loginEmployee'),
                 reverse('loginResident')]
        for page in pages:
            response = self.client.get(page)
            self.assertEqual(response.status_code, 200, f"Page {page} failed to load.")

    def test_admin_access_requires_superuser_status(self):
        """
        Access to the Django admin requires superuser status.
        """
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/admin/')
        self.assertNotEqual(response.status_code, 200)
        self.client.logout()

        self.client.login(username='admin', password='testpass123')
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)

    def test_user_deletion(self):
        """
        Confirm that a user can be deleted and is no longer accessible.
        """
        user_count_initial = User.objects.count()
        self.client.post(reverse('delete_user', args=[self.user.id]))  # Assuming you have a view for deleting users
        user_count_final = User.objects.count()
        self.assertEqual(user_count_initial - 1, user_count_final)

    def test_unauthorized_access_to_admin(self):
        """
        Unauthorized users should not access the admin page.
        """
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/admin/')
        self.assertNotEqual(response.status_code, 200)

    def test_logout_using_get_method(self):
        """
        Logging out using a GET request to ensure the user is logged out.
        """
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('logout'), follow=True)
        self.assertRedirects(response, reverse('homepage'))

    def test_csrf_protection(self):
        """
        Forms should have CSRF tokens for protection against CSRF attacks.
        """
        response = self.client.get(reverse('signup_resident'))
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_session_data_persistence(self):
        """
        Session data should persist across requests.
        """
        session = self.client.session
        session['test_key'] = 'test_value'
        session.save()

        response = self.client.get(reverse('homepage'))
        self.assertEqual(self.client.session['test_key'], 'test_value')


