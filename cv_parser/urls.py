# cv_parser/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_cv, name='upload_cv'),
]
