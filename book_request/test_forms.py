from django.test import TestCase
from .forms import BookRequestForm
from django.contrib.auth.models import User

class BookRequestFormTest(TestCase):

    def setUp(self):
        """
        Create a user to associate with the BookRequest,
        Registered User is required for form submission.
        """
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_book_request_form_valid(self):
        """
        Test the form with valid data
        """
        form_data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'published_year': 2022,
            'description': 'Test Description'
        }
        form = BookRequestForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_book_request_form_invalid(self):
        """
        Test the form with invalid data
        Title is required, so we will not submit a title,
        this should cause the form to be invalid
        """
        form_data = {
            'title': '', 
            'author': 'Test Author',
            'published_year': 2022,
            'description': 'Test Description'
        }
        form = BookRequestForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
    