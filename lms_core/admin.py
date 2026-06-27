from django.contrib import admin
from .models import (
    Course, Lesson, Enrollment, Progress, 
    Quiz, Question, Answer, QuizAttempt, 
    Review, Certificate
)

# Inlines for better admin experience
class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 3

class QuestionInline(admin.StackedInline):
    model = Question
    inlines = [AnswerInline]
    extra = 1

# Admin registrations
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'description')
    inlines = [LessonInline]

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)
    search_fields = ('title', 'content')

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'lesson')
    inlines = [QuestionInline]

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'enrolled_at')
    list_filter = ('course', 'user')

@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'completed')
    list_filter = ('user', 'lesson__course')

@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'score', 'attempted_at')
    list_filter = ('user', 'quiz')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('course', 'user', 'rating', 'created_at')
    list_filter = ('course', 'user', 'rating')

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'date_issued')
    list_filter = ('course', 'user')

# These models are better managed inline, but we can register them for direct access if needed
# admin.site.register(Question)
# admin.site.register(Answer)
