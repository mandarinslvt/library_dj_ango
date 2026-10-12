from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    # Связь один-к-одному со стандартной моделью User (при удалении юзера удаляется профиль)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name="Пользователь")
    
    # Поля, которые могут быть пустыми
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Телефон")
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name="Адрес")
    birth_date = models.DateField(blank=True, null=True, verbose_name="Дата рождения")
    
    # Уникальный номер читательского билета, может быть пустым
    library_card = models.CharField(max_length=50, unique=True, blank=True, null=True, verbose_name="Номер читательского билета")
    
    # Дата регистрации создается автоматически
    registration_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self):
        return f"Профиль {self.user.username}"
