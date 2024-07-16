from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import BookRequestForm
from .models import BookRequest

def book_request(request):
    """
    Renders a form for users to be able to request
    a new book they want to see on the site
    
    Displays an individual instance of :model:`book_request.BookRequest`.
    
    **Context**
    ``book_request``
        The most recent instance of :model:`book_request.BookRequest`.
        ``BookRequest form``
        
    **Template**
    :template:'book_request/book_request.html'
    """
    if request.method == "POST":
        bookRequest_form = BookRequestForm(data=request.POST)
        if bookRequest_form.is_valid():
            book_request_instance = bookRequest_form.save(commit=False)
            book_request_instance.user = request.user
            book_request_instance.save()
            messages.add_message(request, messages.SUCCESS, "Thankyou for your book recommendation!")
            return redirect('book_request')
        else:
            messages.add_message(request, messages.ERROR, "Failed to submit your book recommendation, please try again")
    
    bookRequest_form = BookRequestForm()
    
    return render(request, "book_request/book_request.html", {"bookRequest_form": bookRequest_form},)