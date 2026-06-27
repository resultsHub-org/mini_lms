from django.shortcuts import render
from django.contrib.auth import views as auth_views

def login_selection_view(request):
    """
    Renders a page where the user can choose to log in as an Admin or a Student.
    """
    return render(request, 'authentication/login_selection.html')

class StudentLoginView(auth_views.LoginView):
    """
    A custom login view for students. It uses a specific template.
    """
    template_name = 'authentication/student_login.html'
    # After login, users will be redirected to LOGIN_REDIRECT_URL defined in settings.py
