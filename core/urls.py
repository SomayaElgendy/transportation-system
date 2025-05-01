from django.urls import path
from . import views
from core.api_views import book_ticket_api, my_tickets, trip_list, my_notifications_api
from core.views import staff_view_trips, staff_view_tickets, staff_view_payments, admin_financial_report,view_assigned_trips, report_trip_status, signup_passenger



urlpatterns = [
    path('', views.home, name='home'),
    path('trips/', views.trip_list, name='trip_list'),
    path('book/<int:trip_id>/', views.book_ticket, name='book_ticket'),
    path('booking-success/', views.booking_success, name='booking_success'), 
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('staff-dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('driver-dashboard/', views.driver_dashboard, name='driver_dashboard'),
    path('api/book-ticket/', book_ticket_api, name='book_ticket_api'),
    path('staff/trips/', staff_view_trips, name='staff_view_trips'),
    path('staff/tickets/', staff_view_tickets, name='staff_view_tickets'),
    path('staff/payments/', staff_view_payments, name='staff_view_payments'),
    path('api/my-tickets/', my_tickets, name='my_tickets_api'),
    path('api/trips/', trip_list, name='trip_list_api'),
    path('api/my-notifications/', my_notifications_api, name='my_notifications_api'),
    path('adminn/financial-report/', admin_financial_report, name='admin_financial_report'),
    path('driver/assigned-trips/', view_assigned_trips, name='view_assigned_trips'),
    path('driver/report-trip-status/', report_trip_status, name='report_trip_status'),
    path('signup/', signup_passenger, name='signup'),

]
