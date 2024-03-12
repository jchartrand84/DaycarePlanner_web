# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('menu/', views.menu_view, name='menu'),
    path('daycare_database/', views.daycare_database_view, name='daycare_database'),
    path('update-csv-full/', views.update_csv_full, name='update_csv_full'),
    path('update-csv-single/', views.update_csv_single, name='update_csv_single'),
    path('payment_menu/', views.payment_menu_view, name='payment_menu'),
    path('daycare_scheduler/', views.daycare_scheduler_view, name='daycare_scheduler'),
    path('get_children/', views.get_children, name='get_children'),
    path('get_attendance_records/', views.get_attendance_records, name='get_attendance_records'),
    path('add_attendance_record/', views.add_attendance_record, name='add_attendance_record'),
    path('remove_attendance_record/', views.remove_attendance_record, name='remove_attendance_record'),
    path('check_attendance_record/', views.check_attendance_record, name='check_attendance_record'),
]