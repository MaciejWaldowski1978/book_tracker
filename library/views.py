from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, FavoriteBooks
from .forms import BookForm, RegisterForm

# view lista książek
def book_list(request):
    books = Book.objects.all()
    return render(request, 'library/book_list.html', {'books': books})

# widok szczegolowy ksiazki z rozdzialami
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    chapters = book.chapters.all()  # related_name='chapters' w modelu Chapter
    return render(request, 'library/book_detail.html', {'book': book, 'chapters': chapters})


# dodawanie ksiazek
@login_required
def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)  # pierwsza strona
        if form.is_valid():
            book = form.save(commit=False)
            book.user = request.user  # zalogowany user
            book.save()
            form.save_m2m()  # zapisz relacje wiele-do-wielu (autorzy, kategorie)
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm()
    return render(request, 'library/book_form.html', {'form': form})


# edycja ksiazki
@login_required
def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.user != book.user:
        return redirect('book_detail', pk=book.pk)  # tylko autor moze to edytowac

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm(instance=book)

    return render(request, 'library/book_form.html', {'form': form, 'editing': True})


# usuwanie ksiazki
@login_required
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.user != book.user:
        return redirect('book_detail', pk=book.pk)  # zabezpieczenie

    if request.method == 'POST':
        book.delete()
        return redirect('book_list')

    return render(request, 'library/book_confirm_delete.html', {'book': book})


# szukanie ksiazki bez logowania wymaganego..
def book_search(request):
    query = request.GET.get('q') # Q jest po to aby szukac np autora albo tytulu bez uzycia filra i warunkow
    results = []

    if query:
        results = Book.objects.filter(
            Q(title__icontains=query) |
            Q(authors__name__icontains=query)
        ).distinct() # to jest po to aby szukac po tytule i po autorze w jednym polu

    return render(request, 'library/book_search.html', {'results': results, 'query': query})


# rejestracja nowego usera
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # automatyczne logowanie po rejestracji
            return redirect('book_list')  # przekierowanie na stronę główną
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


# user profil pod faworit
@login_required
def user_profile(request):
    favorites = FavoriteBooks.objects.filter(user=request.user)
    return render(request, 'library/user_profile.html', {'favorites': favorites})

@login_required
def user_profile(request):
    favorites = FavoriteBooks.objects.filter(user=request.user)
    return render(request, 'library/user_profile.html', {'favorites': favorites})

# rejestracja pod wlasny form
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # 🔐 automatyczne logowanie
            return redirect('book_list')  # zmień na inny widok jeśli chcesz
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


# # wlasny logout bo ten w registration nie dziala
# def logout_view(request):
#     logout(request)
#     return redirect('login')

def logout_view(request):
    logout(request)
    return render(request, 'registration/logout.html')
