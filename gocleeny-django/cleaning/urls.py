from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('booking/', views.booking, name='booking'),
    path('bookings/', views.view_bookings, name='view_bookings'),
    path('bookings/<int:booking_id>/edit/', views.edit_booking, name='edit_booking'),
    path('bookings/<int:booking_id>/cancel/', views.cancel_booking, name='cancel_booking'),
    path('careers/', views.careers, name='careers'),
    path('franchise/', views.franchise, name='franchise'),
    path('contact/', views.contact, name='contact'),
]

