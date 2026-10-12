from django.urls import path
from . import views

app_name = 'library'

urlpatterns = [
    path('', views.book_list_view, name='book_list_root'), 
    
    path('books/', views.book_list_view, name='book_list'),
    path('books/<slug:slug>/', views.book_detail_view, name='book_detail'),
    path('authors/', views.author_list_view, name='author_list'),
    path('authors/<int:pk>/', views.author_detail_view, name='author_detail'),
    path('about/', views.about_view, name='about'),
]
