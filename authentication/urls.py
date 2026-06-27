from django.urls import path
from .views import login_selection_view, StudentLoginView
from django.contrib.auth import views as auth_views

app_name = 'authentication'

urlpatterns = [
    path('login/', login_selection_view, name='login_selection'),
    path('login/student/', StudentLoginView.as_view(), name='student_login'),
    # Django's built-in logout view
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'), 
]
