"""
Konfiguracja panelu administracyjnego Django dla aplikacji bibliotecznej.

Zawiera rejestrację modeli Book, Author, Category, Chapter i FavoriteBooks
oraz ich konfigurację dla interfejsu Django Admin.
"""
from django.contrib import admin
from .models import Book, Author, Category, Chapter, FavoriteBooks

# ---- BOOK ADMIN ----
class BookAdmin(admin.ModelAdmin):
    """
    Konfiguracja modelu Book w panelu administratora.

    - Wyświetla tytuł, autorów, kategorie i użytkownika.
    - Umożliwia filtrowanie i wyszukiwanie po tytule, opisie, autorach i kategoriach.
    """
    list_display = ('title', 'get_authors', 'get_categories', 'user')
    search_fields = ['title', 'description', 'authors__name', 'categories__name']
    list_filter = ['category', 'authors', 'user']

    def get_authors(self, obj):
        """Zwraca listę autorów przypisanych do książki jako ciąg tekstowy."""
        return ", ".join([a.name for a in obj.authors.all()])
    get_authors.short_description = 'Autorzy'

    def get_categories(self, obj):
        """ Zwraca listę kategorii przypisanych do książki jako ciąg tekstowy."""
        return ", ".join([c.name for c in obj.category.all()])
    get_categories.short_description = 'Kategorie'

# ---- CHAPTER ADMIN ----
class ChapterAdmin(admin.ModelAdmin):
    """
    Konfiguracja modelu Chapter w panelu administratora.

    - Wyświetla tytuł i powiązaną książkę.
    - Umożliwia filtrowanie i wyszukiwanie po tytule i książce.
    """
    list_display = ('title', 'book')
    search_fields = ['title', 'book__title']
    list_filter = ['book']

# ---- FAVORITE BOOKS ADMIN ----
class FavoriteBooksAdmin(admin.ModelAdmin):
    """
    Konfiguracja modelu FavoriteBooks w panelu administratora.

    - Wyświetla użytkownika i ulubioną książkę.
    - Umożliwia filtrowanie i wyszukiwanie po nazwie użytkownika i tytule książki.
    """
    list_display = ('user', 'book')
    search_fields = ['user__username', 'book__title']
    list_filter = ['user']

# ---- REGISTER MODELS ----
admin.site.register(Book, BookAdmin)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(FavoriteBooks, FavoriteBooksAdmin)
