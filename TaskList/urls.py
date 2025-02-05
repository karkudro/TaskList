from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile_view, name='profile'),  # Главная страница с задачами
    path('complete_task/<int:task_id>/', views.complete_task, name='complete_task'),  # Завершение задачи
    path('delete_task/<int:task_id>/', views.delete_task, name='delete_task'),  # Удаление задачи
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
]

