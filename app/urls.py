from django.urls import path
from . import views

urlpatterns = [
    path('', views.first_home, name='first_home'),
    path('main_home/', views.main_home, name='main_home'),
    path('student/', views.student, name='student'),
    path('edit_student/<int:student_id>/', views.edit_student, name='edit_student'),
    path('delete_student/<int:student_id>/', views.delete_student, name='delete_student'),
    path('view_student/<int:student_id>/', views.view_student, name='view_student'),
    
    
    path('program/', views.program, name='program'),
    path('edit_program/<int:program_id>/', views.edit_program, name='edit_program'),
    path('delete_program/<int:program_id>/', views.delete_program, name='delete_program'),
    
    
]
