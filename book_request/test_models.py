from django.test import TestCase
from django.contrib.auth.models import User
from .models import BookRequest

class BookRequestModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """
        Create a user for testing in the test below.
        """
        cls.user = User.objects.create_user(username='testuser', password='12345')

    def test_create_book_request(self):
        """
        Create a BookRequest instance by filling in and submitting the form
        Check the book request is then created successfully
        Check the 'read' field default is set to False.
        """
        book_request = BookRequest.objects.create(
            title='Test Book',
            author='Test Author',
            published_year=2022,
            description='Test Description',
            user=self.user
        )

        # Test if the book request is created successfully
        self.assertEqual(BookRequest.objects.count(), 1)
        self.assertEqual(book_request.title, 'Test Book')
        self.assertEqual(book_request.author, 'Test Author')
        self.assertEqual(book_request.published_year, 2022)
        self.assertEqual(book_request.description, 'Test Description')
        self.assertEqual(book_request.user, self.user)
        self.assertIsNotNone(book_request.created_on)

        # Check the form default value for field 'read' is set to False
        self.assertEqual(book_request.read, False)
