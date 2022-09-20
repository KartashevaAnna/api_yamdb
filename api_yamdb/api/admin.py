from django.contrib import admin

from reviews.models import Category, Genre, Title, Review, Comment


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    list_filter = ("name", "slug")
    empty_value_display = "-empty-"


class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    list_filter = ("name", "slug")
    empty_value_display = "-empty-"


class TitleAdmin(admin.ModelAdmin):
    list_display = [
        field.name
        for field in Title._meta.get_fields()
        if not field.many_to_many
    ]
    list_filter = ("name", "year", "description")
    empty_value_display = "-empty-"


class ReviewAdmin(admin.ModelAdmin):
    list_display = [
        field.name
        for field in Review._meta.get_fields()
        if not field.many_to_many
    ]
    list_filter = [
        field.name
        for field in Review._meta.get_fields()
        if not field.many_to_many
    ]
    empty_value_display = "-empty-"


class CommentAdmin(admin.ModelAdmin):
    list_display = [
        field.name
        for field in Comment._meta.get_fields()
        if not field.many_to_many
    ]
    list_filter = [
        field.name
        for field in Comment._meta.get_fields()
        if not field.many_to_many
    ]
    empty_value_display = "-empty-"


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
