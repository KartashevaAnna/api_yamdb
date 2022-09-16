from django.db import models
from users.models import User


class Categories(models.Model):
    name = models.CharField(max_length=300)
    slug = models.SlugField(unique=True)


class Genres(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ("id",)


class Titles(models.Model):
    name = models.CharField(max_length=300)
    year = models.IntegerField("Год выпуска")
    rating = models.IntegerField()
    description = models.CharField("Описание", max_length=300)
    genre = models.ManyToManyField(Genres)
    category = models.ForeignKey(Categories, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ("id",)


class Review(models.Model):
<<<<<<< HEAD
    title = models.ForeignKey(Titles, on_delete=models.CASCADE)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)

    class Meta:
        ordering = ("id",)


class Comments(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)

    class Meta:
        ordering = ("id",)
=======
    score = models.PositiveSmallIntegerField()
    text = models.TextField()
    title = models.ForeignKey(
        Titles,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='review'
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique review'
            )
        ]

    def __str__(self):
        return self.text


class Comments(models.Model):
    text = models.TextField()
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    def __str__(self):
        return self.text
>>>>>>> c9c401a (reviws and comments fix)
