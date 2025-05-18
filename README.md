# 📚 Book Tracker

Aplikacja webowa do zarządzania własną biblioteką książek specjalistycznych (finanse, podatki, programowanie, analiza danych).

## 🔍 Funkcjonalności

* ✅ Rejestracja i logowanie użytkowników
* ✅ Dodawanie książek wraz z:

  * opisem
  * autorami (możliwość dodania nowych)
  * kategoriami
  * okładką
* ✅ Edycja i usuwanie książek (tylko przez autora)
* ✅ Dodawanie rozdziałów do książki
* ✅ Przeglądanie szczegółów książki i jej rozdziałów
* ✅ Ulubione książki (dodawanie/usuwanie, widok ulubionych)
* ✅ Wyszukiwarka (po tytule, autorze, opisie, rozdziałach)
* ✅ Widok "Moje książki" oraz "Wszystkie książki"
* ✅ Responsywny interfejs (obsługa desktop i mobile)
* ✅ System autoryzacji (dostęp tylko do wybranych akcji)
* ✅ Testy jednostkowe i integracyjne (Pytest)

## 🛠️ Technologie

* Python 3.12
* Django 5.2
* HTML (z elementami CSS)
* Postgres (domyślna baza danych Django)
* Pytest (testy automatyczne)

## 🚀 Jak uruchomić projekt lokalnie

1. **Sklonuj repozytorium:**

   ```bash
   git clone https://github.com/TwojLogin/book-tracker.git
   cd book-tracker
   ```

2. **Utwórz i aktywuj środowisko wirtualne:**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Mac/Linux
   .venv\Scripts\activate     # Windows
   ```

3. **Zainstaluj zależności:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Uruchom migracje i serwer:**

   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

5. **Zaloguj się / zarejestruj i korzystaj!**

## 🧪 Testy

Aby uruchomić testy:

```bash
pytest
```

## 🖼️ Zrzuty ekranu (opcjonalnie dodaj pliki PNG do folderu static/images i wstaw):

* Strona główna
* Formularz dodania książki
* Widok książki z rozdziałami
* Ulubione książki

## 👨‍💼 Autor

Maciej Waldowski
Python Developer (CodersLab 2025)
