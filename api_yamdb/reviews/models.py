import datetime

from django.db import models
from users.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Categories(models.Model):
    name = models.CharField(
        max_length=256, verbose_name="Категория", help_text="Укажите категорию"
    )
    slug = models.SlugField(
        max_length=50,
        verbose_name="Уникальный ключ",
        unique=True,
        help_text="Укажите уникальный ключ для категории",
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]


class Genres(models.Model):
    name = models.CharField(
        max_length=256, verbose_name="Жанр", help_text="Укажите жанр"
    )
    slug = models.SlugField(
        max_length=50,
        verbose_name="Уникальный ключ",
        unique=True,
        help_text="Укажите уникальный ключ жанра",
    )

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Titles(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name="Название",
        help_text="Укажите название произведения",
    )
    year = models.IntegerField(
        verbose_name="Год выпуска",
        validators=[MaxValueValidator(datetime.datetime.now().year)],
        help_text="Укажите год выпуска произведения",
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name="Описание",
        help_text="Укажите описание произведения",
    )
    genre = models.ManyToManyField(
        Genres,
        blank=True,
        verbose_name="Жанр произведения",
        related_name="titles",
        help_text="Укажите жанр произведения",
    )
    category = models.ForeignKey(
        Categories,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Категория произведения",
        related_name="titles",
        help_text="Укажите категорию произведения",
    )

    class Meta:
        verbose_name = ("Произведение",)
        verbose_name_plural = "Произведения"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Titles,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Произведение",
    )
    text = models.TextField("Текст отзыва")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Пользователь",
    )
    score = models.IntegerField(
        "Оценка", validators=[MaxValueValidator(10), MinValueValidator(1)]
    )
    pub_date = models.DateTimeField("Дата отзыва", auto_now_add=True)

    class Meta:
        ordering = ("pub_date",)
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        constraints = [
            models.UniqueConstraint(
                fields=["author", "title"],
                name="unique_review",
            )
        ]


class Comments(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Отзыв",
    )
    text = models.TextField("Текст комментария")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Пользователь",
    )
    pub_date = models.DateTimeField("Дата комментария", auto_now_add=True)

    class Meta:
        ordering = ("pub_date",)
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
