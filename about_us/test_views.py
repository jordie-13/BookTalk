from django.test import TestCase, Client
from django.urls import reverse
from datetime import datetime
from .models import About_Us

class AboutUsViewTest(TestCase):

    def setUp(self):
        # Create a sample About_Us instance for testing
        self.about_us_entry = About_Us.objects.create(
            title='Sample Title',
            content='Sample content for the About Us page.',
            profile_image='sample_image.jpg',  # Replace with a valid image path or URL
            updated_on=datetime.now()
        )

        # Initialize Django test client
        self.client = Client()

    def test_about_us_view(self):
        """
        Test the about_us view function
        """
        # Make a GET request to the about_us view
        response = self.client.get(reverse('about_us'))

        # Assert that the response is successful (status code 200)
        self.assertEqual(response.status_code, 200)

        # Assert that the correct template is used
        self.assertTemplateUsed(response, 'about_us/about_us.html')

        # Assert that the context contains the correct about_us instance
        self.assertEqual(response.context['about_us'], self.about_us_entry)

    def tearDown(self):
        # Clean up after tests if needed
        self.about_us_entry.delete()
