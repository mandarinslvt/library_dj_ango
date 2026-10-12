from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from .models import Book, Author

def book_list_view(request):
    books = Book.objects.filter(is_available=True).select_related('author')
    return render(request, 'library/book_list.html', {'books': books})

def book_detail_view(request, slug):
    book = get_object_or_404(Book, slug=slug, is_available=True)
    return render(request, 'library/book_detail.html', {'book': book})

def author_list_view(request):
    authors = Author.objects.annotate(books_count=Count('books'))
    return render(request, 'library/author_list.html', {'authors': authors})

def author_detail_view(request, pk):
    author = get_object_or_404(Author, pk=pk)
    books = author.books.filter(is_available=True)
    return render(request, 'library/author_detail.html', {'author': author, 'books': books})

def about_view(request):
    return render(request, 'library/about.html', {'title': 'О библиотеке'})