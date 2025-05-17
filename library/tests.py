from django.test import TestCase

# Create your tests here.
import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from library.models import Book, Author, Category, Chapter, FavoriteBooks

#  logowanie
@pytest.mark.django_db
def test_user_login_redirect(client):
    user = User.objects.create_user(username='testuser', password='StrongPassword123')
    response = client.post(reverse('login'), {
        'username': 'testuser',
        'password': 'StrongPassword123',
    })
    assert response.status_code == 302
    assert response.url == reverse('book_list')

#  autentyfikacja
@pytest.mark.django_db
def test_user_login_authenticated(client):
    user = User.objects.create_user(username='testuser', password='StrongPassword123')

    client.post(reverse('login'), {
        'username': 'testuser',
        'password': 'StrongPassword123',
    })

    response = client.get(reverse('book_list'))
    assert response.wsgi_request.user.is_authenticated

# dodawanie ksiazki dla zalogowanego usera
@pytest.mark.django_db
def test_add_book_authenticated_user(client):
    # Tworzenie użytkownika i logowanie
    user = User.objects.create_user(username='testuser', password='StrongPass123')
    client.login(username='testuser', password='StrongPass123')

    # Tworzenie autora i kategorii (wymagane do ManyToMany)
    author = Author.objects.create(name='Autor Testowy')
    category = Category.objects.create(name='Kategoria Testowa')

    # Dane formularza do POST
    data = {
        'title': 'Testowa książka',
        'description': 'Opis książki',
        'authors': [author.id],
        'category': [category.id],
    }

    # Wysłanie POST do widoku dodawania książki
    response = client.post(reverse('book_add'), data)

    # Sprawdzenie przekierowania (zakładamy na listę książek)
    assert response.status_code == 302
    assert response.url == reverse('book_list')

    # Sprawdzenie czy książka została dodana do bazy
    book = Book.objects.get(title='Testowa książka')
    assert book.description == 'Opis książki'
    assert user == book.user
    assert author in book.authors.all()
    assert category in book.category.all()


#  sprawdzenie czy nie zalogowany moze dodac ksiazke..
@pytest.mark.django_db
def test_book_add_requires_login(client):
    url = reverse('book_add')
    response = client.get(url)

    # Sprawdzenie przekierowania na stronę logowania
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))
    assert 'next=' in response.url  # upewniamy się, że Django zachował redirect back


#  teraz test na listing ksiazek

@pytest.mark.django_db
def test_book_list_view(client):
    # Przygotowanie danych testowych
    author = Author.objects.create(name='Autor Testowy')
    Book.objects.create(title='Książka 1', description='Opis', user=None)
    Book.objects.create(title='Książka 2', description='Opis', user=None)

    # Wysyłamy GET do widoku listy książek
    url = reverse('book_list')
    response = client.get(url)

    # Sprawdzamy odpowiedź
    assert response.status_code == 200
    assert 'Książka 1' in response.content.decode()
    assert 'Książka 2' in response.content.decode()


#  testowanie widoku szczeguly ksiazki
@pytest.mark.django_db
def test_book_detail_view(client):
    # Przygotowanie danych
    user = User.objects.create_user(username='maciej', password='password123')
    author = Author.objects.create(name='Testowy Autor')
    book = Book.objects.create(title='Testowa Książka', description='Opis książki', user=user)
    book.authors.add(author)

    # Pobranie URL do szczegółów książki
    url = reverse('book_detail', args=[book.pk])
    response = client.get(url)

    # Sprawdzenie odpowiedzi
    assert response.status_code == 200
    assert 'Testowa Książka' in response.content.decode()
    assert 'Opis książki' in response.content.decode()
    assert 'Testowy Autor' in response.content.decode()


# usuwanie ksiazki zautoryzowany
@pytest.mark.django_db
def test_book_delete_view_authorized(client):
    # Tworzymy użytkownika i logujemy go
    user = User.objects.create_user(username='owner', password='password123')
    client.login(username='owner', password='password123')

    # Tworzymy książkę i przypisujemy ją temu użytkownikowi
    book = Book.objects.create(title='Usuwalna książka', description='Do usunięcia', user=user)

    # Wywołujemy żądanie GET do potwierdzenia usunięcia
    url = reverse('book_delete', args=[book.pk])
    response = client.get(url)
    assert response.status_code == 200
    assert 'Usuń' in response.content.decode()

    # Wysyłamy żądanie POST do faktycznego usunięcia
    response = client.post(url)
    assert response.status_code == 302  # przekierowanie po usunięciu
    assert Book.objects.filter(pk=book.pk).count() == 0  # książka faktycznie usunięta

# usuwanie ksiazki nie zautoryzowany
@pytest.mark.django_db
def test_book_delete_view_unauthorized(client):
    # Inny użytkownik niż właściciel
    owner = User.objects.create_user(username='owner', password='password123')
    other_user = User.objects.create_user(username='not_owner', password='pass456')

    # Tworzymy książkę przypisaną do ownera
    book = Book.objects.create(title='Cudza książka', description='Nie usuwaj mnie', user=owner)

    # Loguje się inny użytkownik
    client.login(username='not_owner', password='pass456')

    # Próbuje usunąć cudzą książkę
    url = reverse('book_delete', args=[book.pk])
    response = client.post(url)

    # Oczekujemy przekierowania do szczegółów książki, bez usuwania
    assert response.status_code == 302
    assert Book.objects.filter(pk=book.pk).exists()

# test na dodawanie rozdzialow dla wlasciciela ksiazki
@pytest.mark.django_db
def test_add_chapter_as_owner(client):
    user = User.objects.create_user(username='owner', password='testpass')
    client.login(username='owner', password='testpass')

    book = Book.objects.create(title='Książka', description='Opis', user=user)

    url = reverse('add_chapter', args=[book.id])
    response = client.post(url, {
        'title': 'Nowy rozdział',
        'content': 'Treść rozdziału'
    })

    assert response.status_code == 302  # przekierowanie po dodaniu
    assert Chapter.objects.filter(book=book, title='Nowy rozdział').exists()


# test na dodawanie rozdzialow dla nie wlasciciela ksiazki
@pytest.mark.django_db
def test_add_chapter_as_not_owner(client):
    owner = User.objects.create_user(username='owner', password='testpass')
    other_user = User.objects.create_user(username='not_owner', password='pass')
    book = Book.objects.create(title='Książka', description='Opis', user=owner)

    client.login(username='not_owner', password='pass')
    url = reverse('add_chapter', args=[book.id])
    response = client.get(url)

    # assert response.status_code == 404  # brak dostępu, książka nie należy do użytkownika
    assert response.status_code == 200
    assert 'Nie możesz dodać rozdziału' in response.content.decode()

#  test na dodawanie do ulubionych dla zalogowanego
@pytest.mark.django_db
def test_add_book_to_favorites(client):
    user = User.objects.create_user(username='maciek', password='tajnehaslo')
    client.login(username='maciek', password='tajnehaslo')

    book = Book.objects.create(title='Ulubiona', description='Opis', user=user)

    url = reverse('add_to_favorites', args=[book.id])
    response = client.get(url)

    assert response.status_code == 302
    assert FavoriteBooks.objects.filter(user=user, book=book).exists()

#  test na dodawanie do ulubionych dla nie zalogowanego
@pytest.mark.django_db
def test_add_book_to_favorites_unauthenticated(client):
    user = User.objects.create_user(username='user', password='pass')
    book = Book.objects.create(title='Test', description='Opis', user=user)

    url = reverse('add_to_favorites', args=[book.id])
    response = client.get(url)

    # powinien przekierowac do logowania
    assert response.status_code == 302
    assert '/accounts/login/' in response.url

#  test na wyszukanie ksiazki (parametr get)
@pytest.mark.django_db
def test_book_search_returns_matching_books(client):
    # Przygotowanie przykladowychdanych ksiazka python dla poczatkujacych i django zaawansowanych
    user = User.objects.create_user(username='user1', password='pass')
    book1 = Book.objects.create(title='Python dla początkujacych', description='Podstawy języka', user=user)
    book2 = Book.objects.create(title='Zaawansowany Django', description='Framework webowy', user=user)

    # szukanie ksiazki po fragmencie z tytulu
    response = client.get(reverse('book_search'), {'q': 'Python'})

    # Sprawdzenie wynikow
    assert response.status_code == 200
    content = response.content.decode() # decode() bo sa polskie znaki..
    assert 'Python dla początkujacych' in content
    assert 'Zaawansowany Django' not in content


#  test wyszukiwanie po wielu polach:
#  po autorze, po ksiazce, po rozdziale
@pytest.mark.django_db
def test_book_search_multiple_fields(client):
    user = User.objects.create_user(username='user1', password='pass')

    # po autor
    author = Author.objects.create(name='Jan Kowalski')

    # po ksiazce
    book = Book.objects.create(title='Testowa ksiazka', description='To jest opis testowy', user=user)
    book.authors.add(author)

    # rozdziale
    Chapter.objects.create(title='Wprowadzenie', content='Treść rozdziału o testach', book=book)

    # i testy....
    # T1: szukaj po tytule
    response = client.get(reverse('book_search'), {'q': 'Testowa'})
    assert response.status_code == 200
    assert 'Testowa ksiazka' in response.content.decode()

    # T2: szukaj po opisie
    response = client.get(reverse('book_search'), {'q': 'opis testowy'})
    assert 'Testowa ksiazka' in response.content.decode()

    # T3: szukaj po autorze
    response = client.get(reverse('book_search'), {'q': 'Kowalski'})
    assert 'Testowa ksiazka' in response.content.decode()

    # T4: szukaj po tytule rozdziału
    response = client.get(reverse('book_search'), {'q': 'Wprowadzenie'})
    assert 'Testowa ksiazka' in response.content.decode()

    # T5: szukaj po treści rozdziału
    response = client.get(reverse('book_search'), {'q': 'testach'})
    assert 'Testowa ksiazka' in response.content.decode()