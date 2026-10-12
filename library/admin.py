from django.contrib import admin
from django.db.models import Count
from .models import Author, Genre, Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    # В списке — имя, фамилия, дата рождения
    list_display = ('first_name', 'last_name', 'birth_date')
    # Поиск — по имени и фамилии
    search_fields = ('first_name', 'last_name')
    # Фильтр справа — по дате рождения (по годам)
    list_filter = ('birth_date',)
    # Порядок по умолчанию — по фамилии
    ordering = ('last_name',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    # В списке — название, slug, количество книг в жанре
    list_display = ('name', 'slug', 'book_count')
    # Поиск — по названию
    search_fields = ('name',)
    # Slug заполняется автоматически из названия при вводе в форме
    prepopulated_fields = {'slug': ('name',)}

    # Оптимизируем запрос к БД через annotate, чтобы избежать проблемы N+1
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(books_count_annotated=Count('books'))

    # Метод для отображения кастомной колонки
    @admin.display(description='Количество книг в жанре')
    def book_count(self, obj):
        return obj.books_count_annotated


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # В списке — название, автор, год, цена, доступность
    list_display = ('title', 'author', 'year', 'price', 'is_available')
    
    # Цена и доступность редактируются прямо в списке
    # (Поле 'title' не должно быть здесь первым, чтобы оставаться ссылкой)
    list_editable = ('price', 'is_available')
    
    # Поиск — по названию и описанию
    search_fields = ('title', 'description')
    
    # Фильтры справа — по доступности, по автору, по жанру
    list_filter = ('is_available', 'author', 'genres')
    
    # Slug заполняется автоматически из названия
    prepopulated_fields = {'slug': ('title',)}
    
    # Поля «дата добавления» и «дата обновления» — только для чтения
    readonly_fields = ('created_at', 'updated_at')
    
    # Вверху — навигация по датам добавления
    date_hierarchy = 'created_at'

    # Оптимизация N+1: подтягиваем связанного автора (ForeignKey) и жанры (ManyToMany) одним запросом
    list_select_related = ('author',)
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # prefetch_related используется для связей ManyToMany
        return queryset.prefetch_related('genres')

    # Форма редактирования разбита на группы полей (fieldsets)
    # Группа «Служебное» сделана сворачиваемой ('classes': ('collapse',))
    fieldsets = (
        ('Основное', {
            'fields': ('title', 'slug', 'description', 'pages')
        }),
        ('Автор и жанры', {
            'fields': ('author', 'genres')
        }),
        ('Издание', {
            'fields': ('year', 'isbn')
        }),
        ('Цена и наличие', {
            'fields': ('price', 'is_available')
        }),
        ('Служебное', {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at')
        }),
    )