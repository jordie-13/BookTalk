from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from .forms import UserProfileForm
from books.models import Bookshelf, Book


@login_required
def profile(request):
    if request.method == 'POST' and 'profile_form' in request.POST:
        form = UserProfileForm(request.POST, instance=request.user)
        print("Form Data:", request.POST)
        print("Form Instance:", form.instance)
        print("Form Errors before validation:", form.errors)
        if form.is_valid():
            print("Form is valid")
            user = form.save(commit=False)
            new_password = form.cleaned_data.get('new_password')
            if new_password:
                user.set_password(new_password)
                update_session_auth_hash(request, user)  
            user.save()
            print("Profile updated:", user.first_name, user.last_name, user.email)
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('profile')  
        else:
            print("Form is not valid. Errors:", form.errors)
            messages.error(request, 'Please correct the error below.')
    else:
        form = UserProfileForm(instance=request.user)

    # Post request in status form 
    if request.method == 'POST' and 'status_form' in request.POST:
        book_slug = request.POST.get('book_slug')
        status = request.POST.get('status')
        book = get_object_or_404(Book, slug=book_slug)
        bookshelf = get_object_or_404(Bookshelf, book=book, user=request.user)
        bookshelf.status = status
        bookshelf.save()
        return redirect('profile')
    
    bookshelf = Bookshelf.objects.filter(user=request.user)
    status_choices = Bookshelf.STATUS_CHOICES
    books_in_bookshelf = Book.objects.filter(bookshelf__in=bookshelf)
    
    # Prepare a list of dictionaries with book and status
    books_with_status = []
    for entry in bookshelf:
        books_with_status.append({
            'book': entry.book,
            'status': entry.get_status_display(),
        })
    
    # Pagination
    paginator = Paginator(books_in_bookshelf, 4)
    page = request.GET.get('page')
    try:
        books_in_bookshelf = paginator.page(page)
    except PageNotAnInteger:
        books_in_bookshelf = paginator.page(1)
    except EmptyPage:
        books_in_bookshelf = paginator.page(paginator.num_pages)
    
    return render(request, 'profile_page.html', {
        'form': form, 
        'bookshelf': bookshelf,
        'books_in_bookshelf': books_in_bookshelf,
        'books_with_status': books_with_status,
        'status_choices': status_choices,
    })
        
