from django.db import models
from django.contrib.auth import get_user_model
from django.core import validators

User = get_user_model()


class Tag(models.Model):
    """Модель тэгов."""
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название',
        db_index=True)
    color = models.CharField(
        max_length=7,
        unique=True,
        verbose_name='Цветовой HEX-код',
        validators=[
            validators.RegexValidator(
                regex='^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',
                message='Данное значение не является цветом в HEX-формате!'
            )
        ]
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='Уникальный слаг')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Модель ингридиентов."""
    name = models.CharField(
        max_length=200,
        verbose_name='Ингредиент',
        db_index=True)
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единица измерения')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(fields=['name', 'measurement_unit'],
                                    name='unique_name_measurement_unit')
        ]

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Recipe(models.Model):
    """Модель рецептов."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор')
    name = models.CharField(
        max_length=200,
        verbose_name='Название',
        help_text='Введите название рецепта')
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='recipes/')
    text = models.TextField(
        verbose_name='Описание',
        help_text='Введите описание рецепта')
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги')
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientQuantity',
        verbose_name='Ингридиенты',
        related_name='recipes',
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=(
            validators.MinValueValidator(
                1, message='Время приготовления меньше 1 минуты!'),),
        verbose_name='Время приготовления в минутах')
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации')

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientQuantity(models.Model):
    """Модель связи между моделами Ingredient и Recipe."""
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='list_ingredient',
        verbose_name='Ингридиент',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )
    quantity = models.PositiveSmallIntegerField(
        validators=(
            validators.MinValueValidator(
                1, message='Минимальное количество ингридиентов 1!'),),
        verbose_name='Количество',
    )

    class Meta:
        ordering = ('-id', )
        verbose_name = 'Ингредиенты в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'
        constraints = [
            models.UniqueConstraint(fields=['ingredient', 'recipe'],
                                    name='unique_ingredient_recipe')
        ]

    def __str__(self):
        return (
            f'{self.ingredient.name} - {self.quantity}'
            f'  {self.ingredient.measurement_unit}'
        )


class Favorite(models.Model):
    """Модель списка избранного."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт',
    )

    class Meta:
        ordering = ('user',)
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные рецепты'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_recipe_user')
        ]


class Shopping_cart(models.Model):
    """Модель корзины."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Рецепт',
    )

    class Meta:
        ordering = ('user',)
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_user_recipe')
        ]
