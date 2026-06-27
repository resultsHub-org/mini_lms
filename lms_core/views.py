from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Course, Lesson, Enrollment, Progress, Quiz, QuizAttempt, Question, Answer, Review

# Course Views
@login_required
def course_list(request):
    """
    Displays a list of all available courses.
    """
    courses = Course.objects.all()
    return render(request, 'lms_core/course_list.html', {'courses': courses})

def course_detail(request, course_id):
    """
    Displays details for a single course, including its lessons and reviews.
    """
    course = get_object_or_404(Course, pk=course_id)
    # You might want to add logic here to check if the user is enrolled
    return render(request, 'lms_core/course_detail.html', {'course': course})

# Lesson Views
@login_required
def lesson_detail(request, course_id, lesson_id):
    """
    Displays the content of a single lesson.
    Users must be enrolled to view a lesson.
    """
    course = get_object_or_404(Course, pk=course_id)
    lesson = get_object_or_404(Lesson, pk=lesson_id, course=course)

    # Check if the user is enrolled in the course
    if not Enrollment.objects.filter(user=request.user, course=course).exists():
        # You might want to redirect to a different page or show an error
        return redirect('course_detail', course_id=course.id)

    return render(request, 'lms_core/lesson_detail.html', {'lesson': lesson})

# Enrollment and Progress Views
@login_required
def enroll_in_course(request, course_id):
    """
    Enrolls the current user in a course.
    """
    course = get_object_or_404(Course, pk=course_id)
    Enrollment.objects.get_or_create(user=request.user, course=course)
    return redirect('course_detail', course_id=course.id)

@login_required
def mark_lesson_complete(request, lesson_id):
    """
    Marks a lesson as complete for the current user.
    """
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    progress, created = Progress.objects.get_or_create(user=request.user, lesson=lesson)
    progress.completed = True
    progress.save()
    # Redirect to the next lesson or back to the course detail page
    return redirect('course_detail', course_id=lesson.course.id)

# Quiz Views
@login_required
def quiz_detail(request, quiz_id):
    """
    Displays a quiz with its questions.
    """
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    return render(request, 'lms_core/quiz_detail.html', {'quiz': quiz})

@login_required
def submit_quiz(request, quiz_id):
    """
    Processes quiz submissions, calculates the score, and records the attempt.
    """
    if request.method == 'POST':
        quiz = get_object_or_404(Quiz, pk=quiz_id)
        correct_answers = 0
        total_questions = quiz.questions.count()

        for question in quiz.questions.all():
            # The name of the input in the form should be 'question_{{ question.id }}'
            selected_answer_id = request.POST.get(f'question_{question.id}')
            if selected_answer_id:
                answer = get_object_or_404(Answer, pk=selected_answer_id)
                if answer.is_correct:
                    correct_answers += 1
        
        score = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
        
        QuizAttempt.objects.create(user=request.user, quiz=quiz, score=score)

        # Redirect to a results page or back to the lesson
        return redirect('lesson_detail', course_id=quiz.lesson.course.id, lesson_id=quiz.lesson.id)

    # If not a POST request, redirect to the quiz page
    return redirect('quiz_detail', quiz_id=quiz_id)
