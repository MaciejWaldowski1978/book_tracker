from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Book, Chapter, Author

# formlarz ksiazki
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'description', 'cover', 'authors', 'category']
        widgets = {
            'authors': forms.SelectMultiple(attrs={'size': 10}),
            'category': forms.SelectMultiple(attrs={'size': 7}),  # jeśli ManyToMany
        }

# formularz rejestracyjn
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

#formularz dodawania formularzy do ksiazki
class ChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = ['title', 'content']


# dodawanie tylko autora dla uzytkownikow
class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name']
