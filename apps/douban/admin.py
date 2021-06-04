from django.contrib import admin

from apps.douban.models import Movie, Book, Comment, ItemAnalysis


@admin.register(ItemAnalysis)
class ItemAnalysisAdmin(admin.ModelAdmin):
    list_display = ('id', 'dad_id', 'create_date')
    search_fields = ['dad_id']


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'director', 'genre', 'rating_val')
    search_fields = ['id', 'name', 'director', 'actor', 'author', 'genre']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'press', 'rating_val')
    search_fields = ['id', 'name', 'author', 'press']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'comment_type', 'dad_id', 'pub_date')
    search_fields = ('comment_type', 'dad_id')


admin.site.site_title = "ZJ Admin"
admin.site.site_header = "ZJ's Graduation Project admin"
