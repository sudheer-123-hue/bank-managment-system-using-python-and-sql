from django.urls import path
from . import views

urlpatterns = [
    path('', views.movie_list, name='movie_list'),         # handles /movies/
    path('add/', views.add_movie, name='add_movie'),       # handles /movies/add/
    path('book/<int:movie_id>/', views.book_ticket, name='book_ticket'),  # New booking URL
    path('book_seats/<int:movie_id>/', views.book_seats, name='book_seats'),

]
