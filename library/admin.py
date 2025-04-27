from django.contrib import admin
from .models import Book, Author, Category, Chapter, FavoriteBooks

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Chapter)
admin.site.register(FavoriteBooks)
