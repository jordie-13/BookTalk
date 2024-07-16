from django.test import TestCase
from .models import About_Us

class AboutUsModelTest(TestCase):

    def setUp(self):
        """
        Create a sample About_Us instance for testing
        """
        self.about_us_entry = About_Us.objects.create(
            title='Sample Title',
            content='Sample content for the About Us page.',
        )

    def test_about_us_creation(self):
        """
        Test the creation of a new About_Us entry
        """
        # Retrieve the About_Us instance created in setUp()
        about_us_entry = About_Us.objects.get(title='Sample Title')

        # Assert that the attributes of the About_Us instance match the expected values
        self.assertEqual(about_us_entry.title, 'Sample Title')
        self.assertEqual(about_us_entry.content, 'Sample content for the About Us page.')
