# myapp/urls.py
from django.urls import path
from .views import menu_view, daycare_database_view, update_csv  # import the new view

urlpatterns = [
    path('menu/', menu_view, name='menu'),
    path('daycare_database/', daycare_database_view, name='daycare_database'),
    path('update-csv/', update_csv, name='update_csv'),  # add the new url pattern
]