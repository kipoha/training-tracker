from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('', views.workout_list, name='workout_list'),
    path('workout/<int:pk>/', views.workout_detail, name='workout_detail'),
    path('workout/<int:pk>/add_exercise/', views.add_exercise, name='add_exercise'),
    path('add/', views.add_workout, name='add_workout'),
    path('create_exercise/', views.create_exercise, name='create_exercise'),
    path('<int:workout_id>/exercise/<int:exercise_id>/', views.exercise_detail, name='exercise_detail'),
    path('progress_report/', views.progress_report, name='progress_report'),


    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]
