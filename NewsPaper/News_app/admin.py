from django.contrib import admin
from .models import Category, Post, Comment, Author


class PostAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ('author', 'title', 'rating')  # оставляем только имя и цену товара
    list_filter = ('rating', )  # добавляем примитивные фильтры в нашу админку
    search_fields = ('title', 'post_category')  # тут всё очень похоже на фильтры из запросов в базу


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'rating', 'created')
    list_filter = ('user', 'rating')
    search_fields = ('user', 'text')


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user', 'author_rating')
    list_filter = ('user',)
    search_fields = ('user',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Author, AuthorAdmin)
