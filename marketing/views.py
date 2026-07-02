from django.shortcuts import render, redirect

def landing_page_view(request):
    """
    Renders the main landing page of the application, redirecting logged-in students to their portal.
    """
    if request.user.is_authenticated:
        return redirect('lms_core:course_list')
    return render(request, 'marketing/landing.html')

