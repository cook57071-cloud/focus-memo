from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.memo_create, name='memo_create'),
]