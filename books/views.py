from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views import generic
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect, JsonResponse
from django.db.models import Q, Avg, Count
from .models import Book, Comment, Rating, Bookshelf, Genre
from .forms import CommentForm, RatingForm, BookSearchForm

class BookList(generic.ListView):
    model = Book
    template_name = "book_list.html"
    paginate_by = 9

    def get_queryset(self):
        queryset = super().get_queryset()
        # Get the genre ID from the query parameters
        genre_id = self.request.GET.get('genre')
        if genre_id:
            try:
                genre = Genre.objects.get(id=genre_id)
                queryset = queryset.filter(genre=genre)
            except Genre.DoesNotExist:
                pass  
        return queryset

    def get_context_data(self, **kwargs):
        # Add additional context data for rendering the template
        context = super().get_context_data(**kwargs)
        # Retrieve all genres to populate the dropdown menu
        context['genres'] = Genre.objects.all()
        return context

    def post(self, request):
        # Handle POST requests (form submissions)
        # Retrieve the selected genre ID from the form data
        genre_id = request.POST.get('genre')
        if genre_id:
            try:
                genre_name = Genre.objects.get(id=genre_id)
                # Redirect to the 'books' URL with the selected genre ID as a query parameter
                return redirect(reverse('books') + f'?genre={genre_id}&{genre_name}')
            except (ValueError, Genre.DoesNotExist):
                genre_name = None
        # If no valid genre_id or Genre does not exist, return books URL with no filter
        return redirect('books')


def filter_books_by_genre(request):
    genre_id = request.POST.get('genre')
    if genre_id:
        return redirect(reverse('books') + f'?genre={genre_id}')
    return redirect(reverse('books'))


def Homepage(request):
    """
    Display the homepage with the top-rated books.

    **Context**

    ''book_list''
        A queryset containing the top 6 books with the highest average 
        ratings, and excluding books with no ratings.

    **Template:**

    :template:'books/homepage.html'
    """
    top_rated_books = (
        Book.objects.annotate(average_rating=Avg('rater__rating'), rating_count=Count('rater__rating'))
        .filter(rating_count__gt=0) 
        .order_by('-average_rating')[:20]
    )
    context = {'book_list': top_rated_books}
    return render(request, 'homepage.html', context)


def search_books(request):
    """
    Search for books by title, author, or genre.
    
    **Context**
    
    ''form''
        An instance of :form:'books.BookSearchForm'.
    ''books''
        A queryset containing all books that match the search query.
        
    **Template:**
    
    :template:'books/search_books.html'
    """
    form = BookSearchForm(request.GET or None)
    books = Book.objects.all()
    query = None
    
    if form.is_valid():
        query = form.cleaned_data['query']
        if query:
            books = books.filter(
                Q(title__icontains=query) | 
                Q(author__name__icontains=query) | 
                Q(genre__name__icontains=query)
            )
    
    # Pagination
    paginator = Paginator(books, 9) 
    page = request.GET.get('page')
    
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)
        
    return render(request, 'search_books.html', {'form': form, 'query': query, 'book_list': books})
    
    
def book_detail(request, slug):
    """
    Display an individual :model:'books.Book'.
    
    **Context**
    
    ''book''
        An instance of :model:'books.Book'.
    ''comments''
        All comments related to the book.
    ''comment_count''
        Total count of admin approved comments related to the book.
    ''comment_form''
        An instance of :form:'books.CommentForm'.
    ''rating_form''
        An instance of :form:'books.RatingForm'.
        
    **Template:**
    
    :template:'books/book_detail.html'
    """
    
    # Retrieve the book 
    queryset = Book.objects.all()
    book = get_object_or_404(queryset, slug=slug)    
    
    # Check if the book is in the user's bookshelf
    in_bookshelf = False
    if request.user.is_authenticated:
        in_bookshelf = Bookshelf.objects.filter(user=request.user, book=book).exists()
    
    # Retrieve comments 
    comments = book.comments.all().order_by("-created_on")
    comment_count = book.comments.filter(approved=True).count()
    
    # Handle the comment form submission
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.book = book
            comment.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Your comment has been submitted and is awaiting approval'
            )
            print("Comment submitted successfully")
            return HttpResponseRedirect(reverse('book_detail', args=[slug]))
    else:
        # Empty the comment form        
        comment_form = CommentForm()
    
    # Retrieve all ratings for this book 
    book_ratings = Rating.objects.filter(book=book).exclude(rating=-1).values_list('rating', flat=True)
    # Calculate total number of ratings left on the book
    total_ratings = Rating.objects.filter(book=book).count()
    
    # Calculate average rating
    if book_ratings:
        average_rating = sum(book_ratings) / len(book_ratings)
        average_rating = round(average_rating, 1)
    else:
        average_rating = None 
        
    # Handle the rating form submission
    if request.method == "POST":    
        rating_form = RatingForm(data=request.POST)
       
        if rating_form.is_valid():
            rating_value = rating_form.cleaned_data['rating']
            # Get or create a rating object for the user and book
            rating, created = Rating.objects.get_or_create(user=request.user, book=book)
            rating.rating = rating_value
            rating.save()
            print("Rating submitted successfully")
            
            # Calculate the average book rating
            book_ratings = Rating.objects.filter(book=book).exclude(rating=-1).values_list('rating', flat=True)
            if book_ratings:
                average_rating = sum(book_ratings) / len(book_ratings)
                total_ratings = Rating.objects.filter(book=book).count()
            else:
                average_rating = None 
        
            # Check if request was made using AJAX and return a JSON response back to ratings.js submitForm function to be processed. 
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'message': 'Rating submitted successfully', 
                                     'user_rating': rating_value, 
                                     'average_rating': average_rating, 
                                     'total_ratings': total_ratings,
                                     })
            
            # If not an AJAX request, respond with a HTTP response to redirect user to book detail page
            return HttpResponseRedirect(reverse('book_detail', args=[slug]))

    else:
        # Empty the rating form  
        rating_form = RatingForm()
    
    user_rating = None
    # Retrieve the user's rating for the book if the user is authenticated
    if request.user.is_authenticated:
        user_rating_obj = Rating.objects.filter(book=book, user=request.user).first()
        if user_rating_obj:
            user_rating = user_rating_obj.rating

    # Pass variables to the book_detail template            
    return render(request, "books/book_detail.html", {
        "book": book,
        "in_bookshelf": in_bookshelf,
        "comments": comments,
        "comment_count": comment_count,
        "comment_form": comment_form,
        "rating_form": rating_form,  
        "user_rating": user_rating,
        "average_rating": average_rating, 
        "total_ratings": total_ratings,
        },
    )
    

@login_required
def comment_edit(request, slug, comment_id):
    """
    Edit an individual comment related to a book.

    **Context**

    ``book``
        An instance of :model:`books.Book`.
    ``comment``
        A single comment related to the book.
    ``comment_form``
        An instance of :form:`books.CommentForm`.
    """
    if request.method == "POST":
        queryset = Book.objects.all()
        book = get_object_or_404(queryset, slug=slug)
        comment = get_object_or_404(Comment, pk=comment_id)
        comment_form = CommentForm(data=request.POST, instance=comment)

        if comment_form.is_valid() and comment.user == request.user:
            comment = comment_form.save(commit=False)
            comment.book = book
            comment.approved = False
            comment.save()
            messages.add_message(request, messages.SUCCESS, 'Comment Updated!')
            print("Comment edited successfully")
        else:
            messages.add_message(request, messages.ERROR, 'Error, unable to update comment!')
            print("Error: Comment edit failed")

    return HttpResponseRedirect(reverse('book_detail', args=[slug]))


@login_required
def comment_delete(request, slug, comment_id):
    """
    Delete an individual comment related to a book.

    **Context**

    ``book``
        An instance of :model:`books.Book`.
    ``comment``
        A single comment related to the book.
    """
    queryset = Book.objects.all()
    book = get_object_or_404(queryset, slug=slug)
    comment = get_object_or_404(Comment, pk=comment_id)

    if comment.user == request.user:
        comment.delete()
        messages.add_message(request, messages.SUCCESS, 'Comment deleted!')
        print("Comment deleted successfully")
    else:
        messages.add_message(request, messages.ERROR, 'You can only delete your own comments!')
        print("Error: Comment delete failed - not users comment")

    return HttpResponseRedirect(reverse('book_detail', args=[slug]))


# Add and remove books from bookshelf
@login_required
def add_to_bookshelf(request, slug):
    book = get_object_or_404(Book, slug=slug)
    bookshelf_entry, created = Bookshelf.objects.get_or_create(user=request.user, book=book)
    if created:
        bookshelf_entry.status = 'unread'  # default status
        bookshelf_entry.save()
    messages.add_message(request, messages.SUCCESS, 'This book has been added to your Bookshelf!')
    
    return HttpResponseRedirect(reverse('book_detail', args=[slug]))
    

@login_required
def remove_from_bookshelf(request, slug):
    book = get_object_or_404(Book, slug=slug)
    bookshelf_entry = get_object_or_404(Bookshelf, user=request.user, book=book)
    bookshelf_entry.delete()
    messages.add_message(request, messages.SUCCESS, 'This book has been removed from your Bookshelf!')

    # Get the referring URL from the request headers or book_detail if not available
    referer_url = request.META.get('HTTP_REFERER', reverse('book_detail', args=[slug]))

    return HttpResponseRedirect(referer_url)


@login_required
def bookshelf(request):
    bookshelf = Bookshelf.objects.filter(user=request.user)

    # Post request in status form 
    if request.method == 'POST' and 'status_form' in request.POST:
        book_slug = request.POST.get('book_slug')
        status = request.POST.get('status')
        book = get_object_or_404(Book, slug=book_slug)
        bookshelf = get_object_or_404(Bookshelf, book=book, user=request.user)
        bookshelf.status = status
        bookshelf.save()
        return redirect('bookshelf')
    
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
    
    # Calc the number of books in users bookshelf
    bookshelf_total = len(bookshelf)

    # Calculate the number of books the user has marked as read
    books_read_total = bookshelf.filter(status='read').count()

    # Pagination
    paginator = Paginator(books_in_bookshelf, 10)
    page = request.GET.get('page')
    try:
        books_in_bookshelf = paginator.page(page)
    except PageNotAnInteger:
        books_in_bookshelf = paginator.page(1)
    except EmptyPage:
        books_in_bookshelf = paginator.page(paginator.num_pages)
    
    return render(request, 'bookshelf.html', {
        'bookshelf': bookshelf,
        'books_in_bookshelf': books_in_bookshelf,
        'bookshelf_total': bookshelf_total,
        'books_read_total': books_read_total,
        'books_with_status': books_with_status,
        'status_choices': status_choices,
    })
 