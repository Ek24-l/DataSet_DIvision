# arff_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_arff, name='upload_arff'),
]
