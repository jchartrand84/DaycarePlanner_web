# Project3/urls.py
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),  # include the myapp urls
    re_path(r'^.*$', RedirectView.as_view(url='/menu/', permanent=False)),
]
