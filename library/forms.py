from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Book, Chapter

# formlarz ksiazki
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'description', 'cover', 'authors', 'category']

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
