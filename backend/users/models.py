from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

username_validator = RegexValidator(r'^[\w.@+-]+\Z')


class User(AbstractUser):
    """Модель пользователя."""
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name',
    ]
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[username_validator],
        verbose_name='Логин')
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Почта')
    first_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Имя')
    last_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Фамилия')
    password = models.CharField(
        max_length=150,
        verbose_name='Пароль')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Following(models.Model):
    """Модель подписок."""
    user = models.ForeignKey(
        User,
        related_name='follower',
        verbose_name='Подписчик',
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        User,
        related_name='following',
        verbose_name='Автор',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Подписки'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'], name='unique_subscription'
            )
        ]
