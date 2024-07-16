from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import BookRequest
from .forms import BookRequestForm
from django.contrib.messages import get_messages, SUCCESS
from django.contrib import messages

class BookRequestViewTest(TestCase):

    def setUp(self):
        """
        Create a test user
        """
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_book_request_view_get(self):
        """
        Test GET request to the book_request view to render the form
        Check for a successful HTTP request (code:200)
        """
        client = Client()
        response = client.get(reverse('book_request'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book_request/book_request.html')
        self.assertIsInstance(response.context['bookRequest_form'], BookRequestForm)

    def test_book_request_view_post_valid(self):
        """
        Test POST request to the book_request view with valid data
        Check for a successful redirect to book_request.html (Code:302)
        after a successful form submission.
        Ensure the BookRequest ojbect (form submission) is created
        Ensure the correct user is added to the form submission
        """
        client = Client()
        client.force_login(self.user)
        form_data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'published_year': 2022,
            'description': 'Test Description'
        }
        response = client.post(reverse('book_request'), data=form_data)
        self.assertEqual(response.status_code, 302)  
        self.assertEqual(BookRequest.objects.count(), 1) 
        self.assertEqual(BookRequest.objects.first().user, self.user)

    def test_book_request_view_post_invalid(self):
        """
        Test POST request to the book_request view with invalid data
        Title is required, so leaving empty should cause the form to be invalid
        Check for form submission to be denied and stay on same page (code:200)
        Ensure the BookRequest ojbect (form submission) is Not created
        """
        client = Client()
        client.force_login(self.user)
        form_data = {
            'title': '', 
            'author': 'Test Author',
            'published_year': 2022,
            'description': 'Test Description'
        }
        response = client.post(reverse('book_request'), data=form_data)
        self.assertEqual(response.status_code, 200)   
        self.assertEqual(BookRequest.objects.count(), 0)  

    def test_book_request_view_messages(self):
        """
        Test messages displayed after a successful form submission
        Submit a valid form and check message response is correct
        """
        client = Client()
        client.force_login(self.user)
        form_data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'published_year': 2022,
            'description': 'Test Description'
        }
        response = client.post(reverse('book_request'), data=form_data)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Thankyou for your book recommendation!")
