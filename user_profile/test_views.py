from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from books.models import Book, Bookshelf
from user_profile.forms import UserProfileForm
from user_profile.views import profile


class ProfileViewTests(TestCase):

    def setUp(self):
        """
        Create a test user, some book and bookshelf instances for testing
        """
        #Create a test user
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='password')

        # Create some test books and bookshelves
        self.book1 = Book.objects.create(title='Book 1', slug='book-1', published_year='2000')
        self.book2 = Book.objects.create(title='Book 2', slug='book-2', published_year='2000')
        self.bookshelf1 = Bookshelf.objects.create(user=self.user, book=self.book1, status='unread')
        self.bookshelf2 = Bookshelf.objects.create(user=self.user, book=self.book2, status='reading')

        # Initialize Django test client
        self.client = Client()

    def test_profile_view_GET(self):
        """
        Test GET request to profile view
        """
        # Log in the test user and make GET request to profile view
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('profile'))

        # Check response is successful (code: 200) and correct html rendere
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile_page.html')

        # Check that the form is an instance of UserProfileForm
        self.assertIsInstance(response.context['form'], UserProfileForm)

        # Check that both books are in the bookshelf
        self.assertIn(repr(self.bookshelf1), [repr(bookshelf) for bookshelf in response.context['bookshelf']])
        self.assertIn(repr(self.bookshelf2), [repr(bookshelf) for bookshelf in response.context['bookshelf']])


    def test_profile_view_POST_valid_form(self):
        """
        Test POST request to profile view with valid form data
        """
        # Log in the test user and prepare form data
        self.client.login(username='testuser', password='password')
        form_data = {
            'username': 'testuser',
            'first_name': 'Updated First Name',
            'last_name': 'Updated Last Name',
            'email': 'updatedemail@example.com',
            'current_password': 'password',
            'new_password': 'NewPassword123',
            'confirm_password': 'NewPassword123',
            'profile_form': '',  # 'profile_form' key to simulate form submission
        }

        # Make a POST request to the profile view with valid form data
        response = self.client.post(reverse('profile'), data=form_data)

        # Check that the response is a redirect (status code 302)
        self.assertEqual(response.status_code, 302)

        # Check that the profile data has been updated correctly
        updated_user = User.objects.get(username='testuser')
        self.assertEqual(updated_user.first_name, 'Updated First Name')
        self.assertEqual(updated_user.last_name, 'Updated Last Name')
        self.assertEqual(updated_user.email, 'updatedemail@example.com')

        # Check for success message in messages
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Your profile was successfully updated!')

    def test_profile_view_POST_invalid_form(self):
        """
        Test POST request to profile view with invalid form data
        """
        # Log in the test user
        self.client.login(username='testuser', password='password')

        # Prepare invalid form data (invalid email)
        form_data = {
            'username': 'testuser',
            'first_name': 'Updated First Name',
            'last_name': 'Updated Last Name',
            'email': 'invalid-email',  # Invalid email format
            'current_password': 'password',
            'new_password': 'NewPassword123',
            'confirm_password': 'NewPassword123',
            'profile_form': '',  # 'profile_form' key to simulate form submission
        }

        # Make a POST request to the profile view with invalid form data
        response = self.client.post(reverse('profile'), data=form_data)

        # Assert that the response status code is 200 (form submission failed)
        self.assertEqual(response.status_code, 200)

        # Assert that the form instance is invalid
        self.assertFalse(response.context['form'].is_valid())

        # Check for error message in messages
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Please correct the error below.')

    def test_profile_view_POST_status_update(self):
        """
        Test POST request to profile view for updating bookshelf status
        """
        # Log in the test user
        self.client.login(username='testuser', password='password')

        # Prepare status update form data
        book_slug = self.bookshelf1.book.slug
        form_data = {
            'book_slug': book_slug,
            'status': 'finished',
            'status_form': '',  # 'status_form' key to simulate status update
        }

        # Make a POST request to the profile view to update bookshelf status
        response = self.client.post(reverse('profile'), data=form_data)

        # Assert that the response is a redirect (status code 302)
        self.assertEqual(response.status_code, 302)

        # Assert that the bookshelf status has been updated correctly
        updated_bookshelf = get_object_or_404(Bookshelf, user=self.user, book__slug=book_slug)
        self.assertEqual(updated_bookshelf.status, 'finished')


