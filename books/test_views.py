from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from books.models import Book, Comment, Bookshelf, Genre, Author, Rating

class BaseTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        """
        Create test data (users, genres, authors and books) that are common for all tests
        """
        cls.user = User.objects.create_user(username='testuser', password='12345')
        cls.genre = Genre.objects.create(name="Test Genre")
        cls.author = Author.objects.create(name='Test Author')
        cls.book1 = Book.objects.create(title="Book 1", slug="book-1", genre=cls.genre, author=cls.author, published_year='2020')
        cls.book2 = Book.objects.create(title="Book 2", slug="book-2", genre=cls.genre, author=cls.author, published_year='2021')

    @classmethod
    def setUp(cls):
        """
        Create a client/user to use for requests
        """
        cls.client = Client()
        cls.client.force_login(cls.user)  # Simulate logged-in user for all requests


class HomepageViewTest(BaseTestCase):
    def test_homepage_view(self):
        """
        Test the homepage view
        Ensure it renders the html template, successful HTTP request (code:200)
        """
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'homepage.html')
        # Test if book_list is passed in context
        self.assertTrue('book_list' in response.context)


class SearchBooksViewTest(BaseTestCase):
    def test_search_books_view(self):
        """
        Test the search books view without any query
        Check successful HTTP request (code:200)
        """ 
        response = self.client.get(reverse('search_books'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_books.html')
        # Test if form is passed in context
        self.assertTrue('form' in response.context)

    def test_search_books_with_query(self):
        """
        Test the search books view with a query parameter
        Test by using search: Book 1
        Check successful HTTP request (code:200)
        """
        response = self.client.get(reverse('search_books'), {'query': 'Book 1'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_books.html')
        # Test if books matching the query are in context
        self.assertTrue('book_list' in response.context)
        self.assertTrue(len(response.context['book_list']) == 1)


class BookListViewTest(BaseTestCase):
    def test_book_list_view(self):
        """
        Test the book list view without any genre filter
        """
        response = self.client.get(reverse('books'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/book_list.html')
        self.assertTrue('book_list' in response.context_data)
        self.assertTrue('genres' in response.context_data)

    def test_book_list_view_with_genre_filter(self):
        """
        Test the book list view with a genre filter
        """
        response = self.client.get(reverse('books') + f'?genre={self.genre.id}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/book_list.html')
        self.assertTrue('book_list' in response.context_data)
        self.assertTrue('genres' in response.context_data)
        books = response.context_data['book_list']
        for book in books:
            self.assertEqual(book.genre, self.genre)

    def test_book_list_post_request_with_genre(self):
        """
        Test POST request to filter books by genre
        """
        response = self.client.post(reverse('books'), {'genre': self.genre.id})
        self.assertEqual(response.status_code, 302)  # Redirect after form submission
        redirected_url = response.url
        self.assertTrue(redirected_url.startswith(reverse('books')))
        self.assertIn(f'genre={self.genre.id}', redirected_url)

    def test_book_list_post_request_without_genre(self):
        """
        Test POST request without valid genre ID
        """
        response = self.client.post(reverse('books'), {'genre': 'invalid_genre_id'})
        self.assertEqual(response.status_code, 302)  # Redirect after form submission
        redirected_url = response.url
        self.assertTrue(redirected_url.startswith(reverse('books')))















class BookDetailViewTest(BaseTestCase):
    def setUp(self):
        """
        Setup method to create necessary objects for book detail tests
        create a new genre, author, book and comment
        """
        self.genre = Genre.objects.create(name="Genre Test")
        self.author = Author.objects.create(name='Author Test')
        self.book = Book.objects.create(title="Test Book", slug="test-book", genre=self.genre, author=self.author, published_year='2022')
        self.comment = Comment.objects.create(user=self.user, book=self.book, body="Test comment")

    def test_book_detail_view(self):
        """
        Test the book detail view 
        Check successful HTTP request (code:200)
        Check that necesarry variables are passed in context 
        """
        response = self.client.get(reverse('book_detail', args=[self.book.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/book_detail.html')
        # Test if book and other necessary variables are passed in context
        self.assertTrue('book' in response.context)
        self.assertTrue('comment_form' in response.context)
        self.assertTrue('rating_form' in response.context)

    def test_add_to_bookshelf_view(self):
        """
        Test the add to bookshelf view
        Check it redirects (code:302) after a book is added to bookshelf
        """
        response = self.client.get(reverse('add_to_bookshelf', args=[self.book.slug]))
        self.assertEqual(response.status_code, 302)  # Redirects after successful add

    def test_remove_from_bookshelf_view(self):
        """
        Test the remove from bookshelf view
        Check it redirects (code:302) after a book is removed from bookshelf
        """
        Bookshelf.objects.create(user=self.user, book=self.book)
        response = self.client.get(reverse('remove_from_bookshelf', args=[self.book.slug]))
        self.assertEqual(response.status_code, 302)  # Redirects after successful remove

class CommentEditViewTest(BaseTestCase):
    def test_comment_edit_view(self):
        """
        Test the comment edit view
        Check it redirects (code:302) after a comment is edited
        """
        comment = Comment.objects.create(user=self.user, book=self.book1, body="Test comment")
        response = self.client.post(reverse('comment_edit', args=[self.book1.slug, comment.pk]), {'body': 'Edited comment'})
        self.assertEqual(response.status_code, 302)  # Redirects after successful edit

class CommentDeleteViewTest(BaseTestCase):
    def test_comment_delete_view(self):
        """
        Test the comment delete view
        Check it redirects (code:302) after a comment is deleted
        """
        comment = Comment.objects.create(user=self.user, book=self.book1, body="Test comment")
        response = self.client.post(reverse('comment_delete', args=[self.book1.slug, comment.pk]))
        self.assertEqual(response.status_code, 302)  # Redirects after successful delete

class BookshelfViewTest(BaseTestCase):

    def test_bookshelf_view(self):
        """
        Test the bookshelf view 
        For logged in users only.
        Check the profile page html is rendered
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse('bookshelf'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile_page.html')
        # Test if bookshelf is passed in context
        self.assertTrue('bookshelf' in response.context)

    def test_add_to_bookshelf(self):
        """
        Test the add to bookshelf functionality
        Check it redirects (code:302) after added to bookshelf
        """
        response = self.client.get(reverse('add_to_bookshelf', args=[self.book1.slug]))
        self.assertEqual(response.status_code, 302) 

    def test_remove_from_bookshelf(self):
        """
        Test the remove from bookshelf functionality
        Check it redirects (code:302) after removing from bookshelf
        """
        Bookshelf.objects.create(user=self.user, book=self.book1)
        response = self.client.get(reverse('remove_from_bookshelf', args=[self.book1.slug]))
        self.assertEqual(response.status_code, 302)  
