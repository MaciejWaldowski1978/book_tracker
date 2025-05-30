from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, FavoriteBooks, Chapter
from .forms import BookForm, RegisterForm, ChapterForm, AuthorForm
from django.utils.http import url_has_allowed_host_and_scheme
# from django.conf import settings

# === rozwiazanie ostateczne .. i super dziala ===
def book_list(request):
    """Wyświetla listę książek.
    Dla zalogowanych użytkowników z parametrem `mine=true` pokazuje tylko ich książki.
    Dla niezalogowanych lub bez parametru pokazuje wszystkie książki alfabetycznie.
    """
    if request.user.is_authenticated and request.GET.get('mine') == 'true':
        books = Book.objects.filter(user=request.user).order_by('-id')
        show_mine = True
    else:
        books = Book.objects.all().order_by('title')
        show_mine = False

    return render(request, 'library/book_list.html', {
        'books': books,
        'show_mine': show_mine
    })


# ==== detale ksiazki ===
def book_detail(request, pk):
    """Widok szczegółów książki i jej rozdziałów.
    Dla zalogowanych użytkowników pokazuje również status ulubionej książki.
    """
    book = get_object_or_404(Book, pk=pk)
    chapters = book.chapters.all()  # related_name='chapters' w modelu Chapter

    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = FavoriteBooks.objects.filter(user=request.user, book=book).exists()

    return render(request, 'library/book_detail.html', {
        'book': book,
        'chapters': chapters,
        'is_favorite': is_favorite,
    })

# ==== dodawanie ksiazki ===
@login_required
def book_add(request):
    """Widok dodawania nowej książki.
    Dostępny tylko dla zalogowanych użytkowników.
    Sprawdza duplikaty na podstawie tytułu i autorów.
    """
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            # sprawdzenie zeby nie dodac drugi raz tej smej ksiazki tzn tutulu i autora
            title = form.cleaned_data['title']
            authors = form.cleaned_data['authors']
            # existing_books = Book.objects.filter(title=title, user=request.user) # to pozwala dodac ta sam ksiazke do bazy ale innemu uzytkownikowi
            existing_books = Book.objects.all() # to zabezpieczenie jest aby iny uzytkownik nie dodal tej samej ksiazki do bazy
            for book in existing_books:
                if set(book.authors.all()) == set(authors):
                    form.add_error(None, 'Taka książka już istnieje w Twojej bibliotece.')
                    return render(request, 'library/book_form.html', {'form': form})
                    # return render(request, 'library/book_form.html', {'form': form, 'show_back_link': False})
            # zapisanie ksiazki..
            book = form.save(commit=False)
            book.user = request.user  # tylko dla zalogowanych
            book.save()
            form.save_m2m()  # dla ManyToMany: authors
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'library/book_form.html', {'form': form})
    # return render(request, 'library/book_form.html', {'form': form, 'show_back_link': False})


# === edycja ksiazki np rozdzialy ===
@login_required
def book_edit(request, book_id):
    """Edycja książki. Dozwolona tylko dla właściciela książki."""
    book = get_object_or_404(Book, id=book_id, user=request.user)  # tylko właściciel może edytować
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'library/book_form.html', {'form': form,'editing': True})
    # return render(request, 'library/book_form.html', {'form': form, 'editing': True, 'show_back_link': True})


# ==== usuwanie ksiazki ===
@login_required
def book_delete(request, pk):
    """Usuwanie książki. Możliwe tylko przez jej właściciela."""
    book = get_object_or_404(Book, pk=pk)

    if request.user != book.user:
        return redirect('book_detail', pk=book.pk)  # zabezpieczenie

    if request.method == 'POST':
        book.delete()
        return redirect('book_list')

    return render(request, 'library/book_confirm_delete.html', {'book': book})


# ==== szukanie ksiazki bez wymaganego logowania ===
def book_search(request):
    """Wyszukiwarka książek.
    Pozwala wyszukiwać po tytule, opisie, autorze i zawartości rozdziału.
    """
    query = request.GET.get('q') # Q jest po to aby szukac np autora albo tytulu bez uzycia filra i warunkow
    results = []

    if query:
        results = Book.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(authors__name__icontains=query)|
            Q(chapters__title__icontains=query) |
            Q(chapters__content__icontains=query)
        ).distinct() # pomijamy powtarzane wyniki aby nie listowac dwa razy tego samego..

    return render(request, 'library/book_search.html', {'results': results, 'query': query})


# ==== rejestracja nowego uzytkownika ===
def register(request):
    """Rejestracja nowego użytkownika.
    Po poprawnym utworzeniu konta następuje automatyczne logowanie.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # automatyczne logowanie po rejestracji
            return redirect('book_list')  # przekierowanie na stronę główną
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


# ==== profil ulubionych ksiazek ===
@login_required
def user_profile(request):
    """Widok profilu użytkownika z jego ulubionymi książkami."""
    favorites = FavoriteBooks.objects.filter(user=request.user).order_by('book__title')
    return render(request, 'library/user_profile.html', {'favorites': favorites})

# # wlasny loyout bo ten w registration nie dziala
# def logout_view(request):
#     logout(request)
#     return redirect('login')

# ==== wylogowanie uzytkownika ===
def logout_view(request):
    """Wylogowanie użytkownika."""
    logout(request)
    return render(request, 'registration/logout.html')


# === dodawanie rozdzialow ===
@login_required
def add_chapter(request, book_id):
    """Dodawanie rozdziału do książki.
    Możliwe tylko przez właściciela książki.
    """
    book = get_object_or_404(Book, id=book_id)
    # sprawdzamy czy użytkownik ma prawo edytowac ksiazke np gdy zostala dodana pzez inna osobe
    # book = get_object_or_404(Book, id=book_id, user=request.user)
    if book.user != request.user:
        return render(request, 'library/access_denied.html', {
            'message': 'Nie możesz dodać rozdziału do książki, której nie jesteś właścicielem.'
        })

    if request.method == 'POST':
        form = ChapterForm(request.POST)
        if form.is_valid():
            chapter = form.save(commit=False)
            chapter.book = book
            chapter.save()
            return redirect('book_detail', book.id)
    else:
        form = ChapterForm()
    return render(request, 'library/chapter_form.html', {'form': form, 'book': book})


# === Edycja rozdziału  dla autora ===
def edit_chapter(request, pk):
    """Edycja istniejącego rozdziału książki."""
    chapter = get_object_or_404(Chapter, pk=pk)
    if request.method == 'POST':
        form = ChapterForm(request.POST, instance=chapter)
        if form.is_valid():
            form.save()
            return redirect('book_detail', pk=chapter.book.id)
    else:
        form = ChapterForm(instance=chapter)
    return render(request, 'library/chapter_form.html', {'form': form, 'book': chapter.book})

# === Usuwanie rozdziału przez tego samego autora ===
def delete_chapter(request, pk):
    """Usuwanie rozdziału książki przez właściciela."""
    chapter = get_object_or_404(Chapter, pk=pk)
    if request.method == 'POST':
        book_id = chapter.book.id
        chapter.delete()
        return redirect('book_detail', pk=book_id)
    return render(request, 'library/chapter_confirm_delete.html', {'chapter': chapter})


# === dodawania autora ===
@login_required
def add_author(request):
    """Dodawanie nowego autora. Otwiera się w osobnym popupie."""
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('<script>window.close();</script>')  # zamyka popup po dodaniu
    else:
        form = AuthorForm()
    return render(request, 'library/add_author.html', {'form': form})

# === dodaj do ulubionych ===
@login_required
def add_to_favorites(request, book_id):
    """Dodaje książkę do ulubionych dla aktualnie zalogowanego użytkownika."""
    book = get_object_or_404(Book, id=book_id)
    FavoriteBooks.objects.get_or_create(user=request.user, book=book)
    return redirect('book_detail', pk=book.id)


# === usun z ulubionych ===
@login_required
def remove_from_favorites(request, book_id):
    """Usuwa książkę z ulubionych użytkownika."""
    book = get_object_or_404(Book, id=book_id)
    FavoriteBooks.objects.filter(user=request.user, book=book).delete()
    return redirect('book_detail', pk=book.id)


#  zmiana hasla i wylogowanie..
def password_change_done_and_logout(request):
    """Wylogowuje użytkownika po zmianie hasła i wyświetla potwierdzenie."""
    logout(request)
    return render(request, 'registration/password_change_done.html')