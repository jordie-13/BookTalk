from .models import BookRequest
from django import forms

class BookRequestForm(forms.ModelForm):
    """
    Form class for users to request a book
    to be added to the site
    """
    class Meta:
        """
        Specify the book request model and order the fields 
        """
        model = BookRequest
        fields = ('title', 'author', 'published_year', 'description',)
        labels = {
            'title': 'Title',
            'author': 'Author',
            'published_year': 'Published Year',
            'description': 'Description',
        }
        widgets = {
            'description': forms.Textarea(attrs={
                'placeholder': 'Provide a brief summary or details about the book...'
            }),
        }