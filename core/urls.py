from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('trips/', views.trip_list, name='trip_list'),
    path('book/<int:trip_id>/', views.book_ticket, name='book_ticket'),
]
