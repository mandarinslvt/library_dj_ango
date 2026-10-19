from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import Book, Reader

# 1. Список книг
def book_list_view(request):
    books_queryset = Book.objects.filter(is_available=True).select_related('author').order_by('-created_at')
    
    context = {
        'books': books_queryset,
        'title': 'Каталог книг',
        'total_count': books_queryset.count(), 
        'has_books': books_queryset.exists(),   
    }
    return render(request, 'library/book_list.html', context)

# 2. Детальная страница книги
def book_detail_view(request, slug):
    book = get_object_or_404(
        Book.objects.select_related('author').prefetch_related('genres'), 
        slug=slug, 
        is_available=True
    )
    
    context = {
        'book': book,
        'title': book.title, 
        'back_url': reverse('library:book_list'),
    }
    return render(request, 'library/book_detail.html', context)

def reader_list_view(request):
    readers_queryset = Reader.objects.all().order_by('last_name') 
    
    context = {
        'readers': readers_queryset,
        'title': 'Читатели',
        'total_count': readers_queryset.count(),
    }
    return render(request, 'library/reader_list.html', context)

def reader_detail_view(request, pk):
    reader = get_object_or_404(Reader, pk=pk)
    
    context = {
        'reader': reader,
        'title': f'Карточка читателя: {reader.last_name}',
    }
    return render(request, 'library/reader_detail.html', context)
