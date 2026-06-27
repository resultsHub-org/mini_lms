from django.shortcuts import render

def landing_page_view(request):
    """
    Renders the main landing page of the application.
    """
    return render(request, 'marketing/landing.html')
