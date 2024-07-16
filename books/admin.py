from django.contrib import admin
from .models import Author, Book, Comment, Genre, Rating, Bookshelf
from django_summernote.admin import SummernoteModelAdmin



@admin.register(Genre)
class GenreAdmin(SummernoteModelAdmin):
    """
    Lists fields for display in admin, fileds for search,
    and rich-text editor.
    """
    list_display = ('name',)
    search_fields = ['name', 'description']
    summernote_fields = ('description',)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """
    Lists fields for display in admin and fields for search.
    """
    list_display = ('name', 'nationality', 'birth_date',)
    search_fields = ['name']
    
    
@admin.register(Book)
class BookAdmin(SummernoteModelAdmin):
    """
    Lists fields for display in admin, fields for search,
    field filters, fields to prepopulate and rich-text editor.
    """
    list_display = ('title', 'author', 'genre', 'published_year',)
    search_fields = ['title', 'author__name', 'genre__name', 'description']
    list_filter = ('genre', 'created_on',)
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('description',)
    

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """
    Lists fields for display in admin, fields for search,
    field filters,
    """
    search_fields = ['book__title']
    list_filter = ('rating',)
    readonly_fields = ["book", "rating", "user",]
    

@admin.register(Bookshelf)
class BookshelfAdmin(admin.ModelAdmin):
    """
    List fields for display in admin, fields for searching, 
    field filters and list filter.
    """
    list_display = ['user', 'book', 'status']
    search_fields = ['user_username', 'book_title']
    list_filter = ['status', 'user']
    readonly_fields = ["user", "book", "status"]
    
# Register your models here.
admin.site.register(Comment)

