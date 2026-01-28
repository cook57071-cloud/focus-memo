from django.urls import path
from . import views

urlpatterns = [
    path('', views.memo_list, name='memo_list'),
    path('create/', views.memo_create, name='memo_create'),
    path('<int:memo_id>/', views.memo_detail, name='memo_detail'),
    path('<int:memo_id>/edit/', views.memo_update, name='memo_update'),
    path('<int:memo_id>/delete/', views.memo_delete, name='memo_delete'),
    path('<int:memo_id>/update/', views.memo_update, name='memo_update'),

]
