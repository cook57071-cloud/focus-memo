from django.urls import path
from . import views

urlpatterns = [
    path('', views.memo_list, name='memo_list'),  # /memo/
    path('create/', views.memo_create, name='memo_create'),  # /memo/create/
    path('<int:memo_id>/', views.memo_detail, name='memo_detail'),  # /memo/1/
    path('<int:memo_id>/delete/', views.memo_delete, name='memo_delete'),  # /memo/1/delete/
]
