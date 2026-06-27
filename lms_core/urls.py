from django.urls import path
from . import views

# app_name helps Django distinguish between apps with the same URL names
app_name = 'lms_core'

urlpatterns = [
    # Course URLs
    path('', views.course_list, name='course_list'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    
    # Lesson URLs
    path('course/<int:course_id>/lesson/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    
    # Enrollment and Progress URLs
    path('course/<int:course_id>/enroll/', views.enroll_in_course, name='enroll_in_course'),
    path('lesson/<int:lesson_id>/complete/', views.mark_lesson_complete, name='mark_lesson_complete'),

    # Quiz URLs
    path('quiz/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    path('quiz/<int:quiz_id>/submit/', views.submit_quiz, name='submit_quiz'),
]
