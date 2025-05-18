from django.urls import path
from .views import register
from . import views
"""
Mapowanie adresów URL do widoków aplikacji "library".

Ścieżki obejmują:
- wyświetlanie listy i szczegółów książek,
- dodawanie, edycję i usuwanie książek,
- wyszukiwanie i profil użytkownika,
- rejestrację użytkownika,
- dodawanie autorów,
- zarządzanie ulubionymi książkami (dodawanie i usuwanie).

Widoki zabezpieczone dekoratorem `login_required` są dostępne tylko po zalogowaniu.
"""
urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),

    path('book/add/', views.book_add, name='book_add'),
    path('book/<int:pk>/edit/', views.book_edit, name='book_edit'),
    path('book/<int:pk>/delete/', views.book_delete, name='book_delete'),

    path('search/', views.book_search, name='book_search'),
    # path('register/', views.register, name='register'), # to bylo pod register django a nei wlasny formularz
    path('register/', register, name='register'),

    path('profile/', views.user_profile, name='user_profile'),
    path('search/', views.book_search, name='book_search'),

    path('authors/add/', views.add_author, name='add_author'),

    path('book/<int:book_id>/favorite/', views.add_to_favorites, name='add_to_favorites'),
    path('book/<int:book_id>/unfavorite/', views.remove_from_favorites, name='remove_from_favorites'),

]
