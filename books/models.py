import uuid
from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


# Create your models here.
class Genre(models.Model):
    """
    Represents a genre category for books in the library system.
    Each genre has a unique name. 
    Order alphabetically based on 'name'.
    """
    # Fields
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    
    class Meta: 
        ordering =["name"]
    
    def __str__(self):
        return self.name
    
    
class Author(models.Model):
    """
    Represents an author of books in the library system.
    Each author has a unique name
    Order alphabetically based on 'name'.
    """
    # Fields
    name = models.CharField(max_length=50, unique=True)
    birth_date = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=25, blank=True)
    
    class Meta: 
        ordering =["name"]
        
    def __str__(self):
        return self.name
    
    
class Book(models.Model):
    """
    Stores a single book entry related to :model:'books/Genre'
    and :model:'books/Author'. 

    Admin can add book objects to the database via this Model.
    
    Order books in queries defaults to descending order based on 'published_year'.

    Overrides the default save method to ensure each book has a unique slug.
    Raises a ValidationError if attempting to save a book with a non-unique slug.
    """
    # Relationships
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    # Fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=60)
    published_year = models.IntegerField()
    cover_image = CloudinaryField('image', default='placeholder')
    description = models.TextField(max_length= 1000, blank=True, null=True)
    slug = models.SlugField(max_length=60, unique=True, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta: 
        ordering =["-published_year"]
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        
        # Check if the slug is unique; raise ValidationError if not
        if Book.objects.filter(slug=self.slug).exists():
            raise ValidationError('This book already exists in the library.')
        
        super().save(*args, **kwargs)


class Comment(models.Model):
    """
    Stores a single comment entry related to :model:'auth.User'
    and :model:'books/Book'.
    """    
    # Relationships
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="comments")
    # Fields
    body = models.TextField(max_length=1000)
    approved = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["created_on"]
        
    def __str__(self):
       return f"Comment {self.body} by {self.user}"
        

class Rating(models.Model):
    """
    Stores a single rating entry related to :model:'auth.User'
    and :model:'books/Book'.
    
    Each user can rate each book only once. The rating is an integer
    value between 1 and 5 inclusive.
    """
    # Relationships
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ratings")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="rater")
    # Fields
    rating = models.IntegerField(choices=[(i, i) for i in range (1, 6)], default=-1)
    last_updated = models.DateTimeField(auto_now=True)

    """
    Enforces uniqueness constraints on the fields user and book in the model.
    This means the combination of the user and book values must be unique and not already exist. 
    It will make sure a user can rate a particular book only once. 
    """
    class Meta:
        unique_together = ('user', 'book') 
        
    def __str__(self):
        return f'{self.book.title} - {self.rating} Stars - Rated by: {self.user.username}'
    

class Bookshelf(models.Model):
    STATUS_CHOICES = [
        ('read', 'Read'),
        ('unread', 'Unread'),
        ('reading', 'Reading'),
    ]
    STYLE_CHOICES = [
        ('audiobook', 'Audiobook'),
        ('kindle', 'Kindle'),
        ('paper', 'Paper'),
    ]
    # Relationships
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    # Fields
    status = models.CharField(max_length=7, choices=STATUS_CHOICES, default='unread')
    style = models.CharField(max_length=10, choices=STYLE_CHOICES, default='paper')
    notes = models.TextField(max_length=1000, blank=True, null=True)
    quotes = models.TextField(max_length=1000, blank=True, null=True)
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book')  # Ensure each book can only be added once per user

    def __str__(self):
        return f"{self.user.username} - {self.book.title} ({self.get_status_display()})"