from django.contrib import admin
from .models import Category, Course, Lesson, Enrollment, Progress, Announcement

# Inlines for better admin experience
class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1

# Admin registrations
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'code', 'instructor', 'category', 'level', 'is_published', 'created_at')
    list_filter = ('level', 'is_published', 'category', 'instructor')
    search_fields = ('title', 'code', 'description')
    inlines = [LessonInline]

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order', 'is_preview', 'created_at')
    list_filter = ('course', 'is_preview')
    search_fields = ('title', 'description', 'content')

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'enrolled_at', 'completed', 'completed_at')
    list_filter = ('course', 'user', 'completed')

@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'completed', 'completed_at')
    list_filter = ('user', 'lesson__course', 'completed')

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'created_at')
    list_filter = ('course',)
    search_fields = ('title', 'message')
