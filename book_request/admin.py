from django.contrib import admin
from .models import BookRequest

# Register your models here.
@admin.register(BookRequest)
class BookRequestAdmin(admin.ModelAdmin):
    """
    Lists fields for display in admin, fields for search,
    field filters,
    """
    search_fields = ['title', 'user',]
    list_filter = ('read',)
    readonly_fields = ["title", "author", "published_year", "description", "user"]
