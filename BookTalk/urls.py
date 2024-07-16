from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("about_us/", include("about_us.urls"), name="about_us-urls"),
    path("accounts/", include("allauth.urls")),
    path('admin/', admin.site.urls),
    path('book_request/', include("book_request.urls"), name="book_request-urls"),
    path('summernote/', include('django_summernote.urls')),
    path("", include("books.urls"), name="books-urls"),
    path('profile/', include("user_profile.urls"), name="user_profile-urls"),
]
