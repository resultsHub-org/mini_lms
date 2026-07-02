from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import UserCreationForm

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

from django.contrib.auth import login

def student_register_view(request):
    """
    Allows a student to register for an account and automatically logs them in.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('lms_core:course_list')
    else:
        form = UserCreationForm()
    return render(request, 'authentication/student_register.html', {'form': form})

