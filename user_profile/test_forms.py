from django.test import TestCase
from django.contrib.auth.models import User
from .forms import UserProfileForm


class UserProfileFormTests(TestCase):

    def setUp(self):
        """
        Create a test user
        """
        self.user = User.objects.create_user(username='testuser', password='Oldpassword1')

    def test_valid_form_data(self):
        """
        Test to confirm the profile form submits successfully when 
        valid data is submitted
        """
        form_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'example@example.com',
            'current_password': 'Oldpassword1',
            'new_password': 'Newpassword1',
            'confirm_password': 'Newpassword1',
        }
        form = UserProfileForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())

    def test_invalid_current_password(self):
        """
        Test case for an invalid current password
        """
        form_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'example@example.com',
            'current_password': 'wrongpassword',
            'new_password': 'Newpassword2',
            'confirm_password': 'Newpassword2',
        }
        form = UserProfileForm(data=form_data, instance=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('current_password', form.errors)

    def test_new_password_mismatch(self):
        """
        Test case for a new password and confirm password mismatch
        Check for in not valid. Verify that the form validation process
        correctly identifies errors related to the confirm_password field.
        """
        form_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'example@example.com',
            'current_password': 'Oldpassword1',
            'new_password': 'Newpassword',
            'confirm_password': 'Mismatchedpassword',
        }
        form = UserProfileForm(data=form_data, instance=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('confirm_password', form.errors) 
