from datetime import date
from django.test import TestCase
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from books.models import Author, Book, Bookshelf, Comment, Genre, Rating, User

from django.db.utils import IntegrityError

# Create your tests here.
class AuthorModelTest(TestCase):

    def setUp(self):
        """
        Creates two Author objects to be used in test methods below.
        """
        self.author1 = Author.objects.create(name='Test Author', birth_date=date(2000,1,1), nationality='Swedish')
        self.author2 = Author.objects.create(name='Sample Author')

    def test_author_creation(self):
        """
        Test creating an Author object.
        """                             
        # Retrieve the author from the database
        author = Author.objects.get(name="Test Author")

        # Verify the data matches what was saved
        self.assertEqual(author.name, "Test Author")
        self.assertEqual(author.birth_date, date(2000, 1, 1))
        self.assertEqual(author.nationality, "Swedish")

    def test_author_unique_constraint(self):
        """
        Test the unique constraint on Author name.
        Attempt to create another author with the same name
        """
        with self.assertRaises(IntegrityError):
            Author.objects.create(
                name='Test Author',
                birth_date=date(2000, 2, 2),
                nationality='Irish'
            )


class GenreModelTest(TestCase):
        
    def setUp(self):
        """
        Creates two Genre objects to be used in test methods below.
        """
        self.genre1 = Genre.objects.create(name='Thriller', description='Books of thrilling nature')
        self.genre2 = Genre.objects.create(name='Romance')

    def test_genre_creation(self):
        """
        Test creating a Genre object.
        """
        self.assertEqual(self.genre1.name, 'Thriller')
        self.assertEqual(self.genre1.description, 'Books of thrilling nature')
        self.assertEqual(str(self.genre1), 'Thriller') 

    def test_genre_unique_constraint(self):
        """
        Test the unique constraint on Genre name.
        Attempt to create a Genre with the same name as in setUp
        """
        with self.assertRaises(IntegrityError):
            Genre.objects.create(name='Thriller')


class BookModelTest(TestCase):

    def setUp(self):
        """
        Creates test objects (Genre, Author) for testing Book model.
        """
        self.genre = Genre.objects.create(name='Test Genre')
        self.author = Author.objects.create(name='Test Author')

    def test_book_creation(self):
        """
        Test creating a Book object.
        """
        # Create a Book object
        book = Book.objects.create(
            title='Test Book',
            published_year=2020,
            genre=self.genre,
            author=self.author,
            description='This is a test book description.'
        )

        # Retrieve the book from the database
        saved_book = Book.objects.get(title='Test Book')

        # Verify the data matches what was saved
        self.assertEqual(saved_book.title, 'Test Book')
        self.assertEqual(saved_book.published_year, 2020)
        self.assertEqual(saved_book.genre, self.genre)
        self.assertEqual(saved_book.author, self.author)
        self.assertEqual(saved_book.description, 'This is a test book description.')
        self.assertIsNotNone(saved_book.created_on)
        self.assertIsNotNone(saved_book.last_updated)
        # Ensure slug is generated correctly
        self.assertEqual(saved_book.slug, slugify('Test Book'))  

    def test_book_unique_slug(self):
        """
        Test the unique constraint on Book slug.
        Create two books with the same title
        """
        book1 = Book.objects.create(
            title='Test Book',
            published_year=2022,
            genre=self.genre,
            author=self.author,
        )
        
        # Attempt to create another book with the same title
        with self.assertRaises(ValidationError):
            book2 = Book(
                title='Test Book',
                published_year=2021,
                genre=self.genre,
                author=self.author,
            )
            book2.full_clean()  # Trigger validation without saving
            book2.save()  # Save should raise ValidationError due to unique slug constraint

    def test_book_ordering(self):
        """
        Test the default ordering of Book model.
        """
        # Create books with different published years
        book1 = Book.objects.create(
            title='Book 1',
            published_year=2020,
            genre=self.genre,
            author=self.author
        )
        book2 = Book.objects.create(
            title='Book 2',
            published_year=2019,
            genre=self.genre,
            author=self.author
        )
        
        # Retrieve books ordered by published year descending
        books = Book.objects.all()
        self.assertEqual(list(books), [book1, book2])

    def test_book_description_optional(self):
        """
        Test creating a Book object without a description.
        """
        book = Book.objects.create(
            title='Book without Description',
            published_year=2018,
            genre=self.genre,
            author=self.author
        )
        saved_book = Book.objects.get(title='Book without Description')
        self.assertIsNone(saved_book.description)


class CommentModelTest(TestCase):

    def setUp(self):
        """
        Set up a User profile, genre, author and book object.
        Create an approved comment and an unapproved comment.
        Testing the ability to create objects in these models
        and to be used for comment tests
        """
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.genre = Genre.objects.create(name='Romance')
        self.author = Author.objects.create(name='Test Author')
        self.book = Book.objects.create(
            title='Test Book',
            published_year=2000,
            genre=self.genre,
            author=self.author,
        )
        self.comment1 = Comment.objects.create(
            book=self.book,
            user=self.user,
            body='This is a test comment.',
            approved=True
        )
        self.comment2 = Comment.objects.create(
            book=self.book,
            user=self.user,
            body='This is another test comment.',
            approved=False
        )

    def test_comment_ordering(self):
        """
        Test the ordering of comments by created_on.
        """
        comments = Comment.objects.all()
        self.assertEqual(comments[0], self.comment1)
        self.assertEqual(comments[1], self.comment2)

    def test_comment_association(self):
        """
        Test the association of a comment with the specified user and a book.
        """
        self.assertEqual(self.comment1.book.title, 'Test Book')
        self.assertEqual(self.comment1.user.username, 'testuser')

    def test_comment_without_user(self):
        """
        Test that creating a Comment without a User raises an IntegrityError.
        """
        with self.assertRaises(IntegrityError):
            Comment.objects.create(book=self.book, body='This comment has no user.')


class RatingModelTest(TestCase):

    def setUp(self):
        """
        Set up test data for the Rating model.
        Create a User profile, genre, author and book object.
        Create a Rating object. 
        """
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.genre = Genre.objects.create(name='Test Genre')
        self.author = Author.objects.create(name='Test Author', birth_date=date(2000, 1, 1), nationality='Swedish')
        self.book = Book.objects.create(
            title='Test Book',
            published_year=2021,
            genre=self.genre,
            author=self.author,
            slug='test-book'
        )
        self.rating1 = Rating.objects.create(user=self.user, book=self.book, rating=5)

    def test_rating_creation(self):
        """
        Test creating a Rating object.
        Check that the self.rating1 created in setUp stored values correctly
        """
        self.assertEqual(self.rating1.rating, 5)
        self.assertEqual(self.rating1.user, self.user)
        self.assertEqual(self.rating1.book, self.book)

    def test_rating_update(self):
        """
        Test updating a Rating object.
        Change the users rating twice. 
        A user can only have 1 rating stored per book
        """
        self.rating1.rating = 3
        self.rating1.save()
        self.assertEqual(self.rating1.rating, 3)
        self.rating1.rating = 4
        self.rating1.save()
        self.assertEqual(self.rating1.rating, 4)

    def test_unique_user_book_rating(self):
        """
        Test that a user can only rate a book once.
        """
        with self.assertRaises(IntegrityError):
            Rating.objects.create(user=self.user, book=self.book, rating=4)


class BookshelfModelTest(TestCase):

    def setUp(self):
        """
        Set up test data for the Bookshelf model.
        Create a user, genre, author and book object.
        Create a bookshelf entry using these above objects.
        """
        self.user = User.objects.create_user(username='testuser', password='password')
        self.genre = Genre.objects.create(name='Test Genre')
        self.author = Author.objects.create(name='Test Author', birth_date=date(2000, 1, 1), nationality='Swedish')
        self.book = Book.objects.create(
            title='Test Book',
            published_year=2021,
            genre=self.genre,
            author=self.author,
            slug='test-book'
        )
        self.bookshelf_entry = Bookshelf.objects.create(user=self.user, book=self.book)

    def test_bookshelf_creation(self):
        """
        Test creating a Bookshelf object and default status is set to 'unread'
        Check the values were stored correctly when creating self.bookshelf_entry in setUp
        """
        self.assertEqual(self.bookshelf_entry.user, self.user)
        self.assertEqual(self.bookshelf_entry.book, self.book)
        self.assertEqual(self.bookshelf_entry.status, 'unread')

    def test_bookshelf_update_status(self):
        """
        Test updating the status of a Bookshelf object.
        Change self.bookshelf_entry from reading to read.
        Check it updated/stored the status correctly 
        """
        self.bookshelf_entry.status = 'read'
        self.bookshelf_entry.save()
        self.assertEqual(self.bookshelf_entry.status, 'read')

    def test_unique_user_book_bookshelf(self):
        """
        Test that a user can only add a book to their bookshelf once.
        User tries to add the same book and should return an error
        """
        with self.assertRaises(IntegrityError):
            Bookshelf.objects.create(user=self.user, book=self.book, status='unread')

    def test_bookshelf_without_user(self):
        """
        Test creating a Bookshelf object without a user.
        Adding a book to bookshelf without a User should return an error
        """
        with self.assertRaises(IntegrityError):
            Bookshelf.objects.create(book=self.book, status='unread')

    def test_bookshelf_without_book(self):
        """
        Test creating a Bookshelf object without a book.
        Adding a book to bookshelf without a book oobject should return an error
        """
        with self.assertRaises(IntegrityError):
            Bookshelf.objects.create(user=self.user, status='unread')