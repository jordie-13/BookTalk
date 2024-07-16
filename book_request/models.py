from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator


class BookRequest(models.Model):
    """
    Stores a single Book request message.
    For users to request a book to be added to the site
    """
    # Relationships
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="requester")

    # Fields
    title = models.CharField(max_length=60)
    author = models.CharField(max_length=60)
    published_year = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(9999),
            RegexValidator(
                regex=r'^\d{4}$',
                message='Year cannot be more than 4 digits',
                code='invalid_year'
            ),
        ]
    )
    description = models.TextField(blank=True, null=True, max_length=500)
    read = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user} has requested the book: {self.title}"