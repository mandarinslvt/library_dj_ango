from django.db import models

class Author(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    bio = models.TextField(null=True, blank=True, verbose_name="Краткая биография")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания записи")

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="Slug")
    description = models.TextField(null=True, blank=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"
        ordering = ['name']

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="Slug")
    
    author = models.ForeignKey(
        Author, 
        on_delete=models.PROTECT, 
        related_name="books", 
        verbose_name="Автор"
    )
    genres = models.ManyToManyField(Genre, blank=True, related_name="books", verbose_name="Жанры")
    
    year = models.IntegerField(verbose_name="Год издания")
    isbn = models.CharField(max_length=13, unique=True, null=True, blank=True, verbose_name="ISBN")
    description = models.TextField(null=True, blank=True, verbose_name="Краткое описание")
    pages = models.IntegerField(verbose_name="Количество страниц")
    
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    
    is_available = models.BooleanField(default=True, verbose_name="Доступна для выдачи")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
        ordering = ['title']

    def __str__(self):
        return self.title
