from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
    path("", include("books.urls"), name="books-urls"),
    path('profile/', include("user_profile.urls"), name="user_profile-urls"),
    path('summernote/', include('django_summernote.urls')),
]
