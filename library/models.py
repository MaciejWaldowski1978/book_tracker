from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# autorzy
class Author(models.Model):
    """Model reprezentujący autora książki."""
    name = models.CharField(max_length=255)

    def __str__(self):
        """Zwraca nazwę autora jako tekst."""
        return self.name

# tabela z kategoriami
class Category(models.Model):
    """Model reprezentujący kategorię książki (np. programowanie, finanse itd)."""
    name = models.CharField(max_length=255)

    def __str__(self):
        """Zwraca nazwę kategorii jako tekst."""
        return self.name

# Tabela glowna z ksiazkami
class Book(models.Model):
    """Model reprezentujący książkę w bibliotece użytkownika."""
    title = models.CharField(max_length=255)
    description = models.TextField()
    cover = models.ImageField(upload_to='covers/', null=True, blank=True)
    authors = models.ManyToManyField(Author)
    category = models.ManyToManyField(Category)
    # category = models.ForeignKey(Category, on_delete=models.CASCADE) # many to many
    # user = models.ForeignKey(User, on_delete=models.CASCADE) # jak chcesz zaby sie ksiazki uzuwaly jak usuniesz uzytkownika
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self):
        """Zwraca tytuł książki jako tekst."""
        return self.title

# tabela z rozdzialamia
class Chapter(models.Model):
    """Model reprezentujący rozdział przypisany do konkretnej książki."""
    title = models.CharField(max_length=255)
    content = models.TextField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='chapters')

    def __str__(self):
        """Zwraca tytuł rozdziału i tytuł książki."""
        return f"{self.title} ({self.book.title})"

class FavoriteBooks(models.Model):
    """Model reprezentujący ulubione książki danego użytkownika."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'book')  # Każdy użytkownik może mieć daną książkę tylko raz w ulubionych

    def __str__(self):
        """Zwraca informację: użytkownik -> tytuł książki."""
        return f"{self.user.username} -> {self.book.title}"
