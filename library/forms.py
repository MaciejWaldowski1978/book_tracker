from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Book, Chapter, Author


# formlarz ksiazki
class BookForm(forms.ModelForm):
    """
    Formularz do tworzenia i edycji książek.
    Zawiera pola: tytuł, opis, okładka, autorzy, kategorie.
    Pola autorów i kategorii są sortowane alfabetycznie.
    """

    class Meta:
        model = Book
        fields = ['title', 'description', 'cover', 'authors', 'category']
        widgets = {
            'authors': forms.SelectMultiple(attrs={'size': 10}),
            'category': forms.SelectMultiple(attrs={'size': 7}),  # jeśli ManyToMany
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Sortowanie alfabetyczne
        self.fields['authors'].queryset = self.fields['authors'].queryset.order_by('name')
        self.fields['category'].queryset = self.fields['category'].queryset.order_by('name')


# formularz rejestracyjny
class RegisterForm(UserCreationForm):
    """
    Formularz rejestracji użytkownika.
    Rozszerza domyślny formularz Django o pole e-mail.
    """
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


#formularz dodawania rozdzialow do ksiazki
class ChapterForm(forms.ModelForm):
    """
    Formularz do tworzenia i edycji rozdziałów książek.
    Zawiera pola: tytuł i treść.
    """
    class Meta:
        model = Chapter
        fields = ['title', 'content']


# dodawanie tylko autora dla uzytkownikow
class AuthorForm(forms.ModelForm):
    """
    Formularz do dodawania nowych autorów.
    Zawiera jedno pole: imię i nazwisko autora.
    """
    class Meta:
        model = Author
        fields = ['name']
