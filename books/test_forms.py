from django.test import TestCase
from books.forms import CommentForm, RatingForm, BookSearchForm, BookshelfForm
from books.models import Comment, Rating, Bookshelf, User, Book, Genre, Author
from datetime import date

# Set up initial data for the tests.
class BaseTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """
        Set up initial data for all test methods.
        This data cannot be edited in the tests.
        Create a user, genre, author and book object
        """
        cls.user = User.objects.create_user(username='testuser', password='password')
        cls.genre = Genre.objects.create(name='Test Genre')
        cls.author = Author.objects.create(name='Test Author', birth_date=date(2000, 1, 1), nationality='Swedish')
        cls.book = Book.objects.create(
            title='Test Book',
            published_year=2021,
            genre=cls.genre,
            author=cls.author,
            slug='test-book'
        )

# Run tests
class RatingFormTest(BaseTest): 

    def test_rating_form_valid_data(self):
        """
        Test that the form handles valid data inputs
        """
        form_data = {'rating': 5}
        form = RatingForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_rating_form_invalid_data(self):
        """
        Test that the form handles invalid data inputs
        """
        form_data = {'rating': 6}
        form = RatingForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_rating_form_save(self):
        """
        Test that the form saves valid data correctly
        Submit a rating to the RatingForm, 
        Check it is valid data, assign the rating a book and user object,
        save the form rating data as a rating in Rating.
        Check the data submitted was stored correctly
        """
        form_data = {'rating': 4}
        form = RatingForm(data=form_data)
        self.assertTrue(form.is_valid())
        rating = form.save(commit=False)
        rating.user = self.user
        rating.book = self.book
        rating.save()
        self.assertEqual(Rating.objects.count(), 1)
        saved_rating = Rating.objects.first()
        self.assertEqual(saved_rating.rating, 4)
        self.assertEqual(saved_rating.user, self.user)
        self.assertEqual(saved_rating.book, self.book)


class BookSearchFormTest(TestCase):

    def test_book_search_form_valid_data(self):
        """
        Test for validating the BookSearchForm with valid data
        Input a test string 'Test Book' to the search form and
        Check that the form is submitted and validated.
        """
        form_data = {'query': 'Test Book'}
        form = BookSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_book_search_form_empty_data(self):
        """
        Test for validating a search with an empty input
        """
        form_data = {'query': ''}
        form = BookSearchForm(data=form_data)
        self.assertTrue(form.is_valid())


class CommentFormTest(BaseTest):

    def test_comment_form_valid_data(self):
        """
        Test for validating CommentForm with valid data.
        """
        form_data = {'body': 'This is a test comment.'}
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_comment_form_empty_data(self):
        """
        Test for validating CommentForm with empty data.
        If comment is submitted with no comment text should 
        return 'This field is required.' error.
        """
        form = CommentForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('body', form.errors)
        self.assertEqual(form.errors['body'], ['This field is required.'])

    def test_comment_form_body_max_length(self):
        """
        Test for validating CommentForm with body exceeding maximum length set to 1000.
        Submit a comment with 1001 characters. Should return error message
        """
        form_data = {'body': 'a' * 1001}
        form = CommentForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('body', form.errors)
        self.assertEqual(form.errors['body'], ['Ensure this value has at most 1000 characters (it has 1001).'])

    def test_comment_form_save(self):
        """
        Test saving a Comment object using CommentForm.
        Submits a comment and checks it is valid (contains text).
        Adds user and book objects to the Comment object and saves it.
        Checks the submitted data is saved correctly in the Rating model.
        """
        form_data = {'body': 'This is a test comment.'}
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())
        comment = form.save(commit=False)
        comment.user = self.user
        comment.book = self.book
        comment.save()
        self.assertEqual(Comment.objects.count(), 1)
        saved_comment = Comment.objects.first()
        self.assertEqual(saved_comment.body, 'This is a test comment.')
        self.assertEqual(saved_comment.user, self.user)
        self.assertEqual(saved_comment.book, self.book)
