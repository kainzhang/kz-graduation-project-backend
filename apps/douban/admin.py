from django.contrib import admin

from apps.douban.models import Movie, Book, Comment, ItemAnalysis


@admin.register(ItemAnalysis)
class ItemAnalysisAdmin(admin.ModelAdmin):
    list_display = ('id', 'dad_id', 'create_date')


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'director', 'genre', 'rating_val')


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'press', 'rating_val')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'comment_type', 'dad_id', 'pub_date')
