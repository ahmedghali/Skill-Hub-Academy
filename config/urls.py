"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.shortcuts import render
from django.urls import include, path
from django.contrib.auth.views import LoginView, LogoutView
from apps.core.views import *
from apps.courses.views import *
from apps.enrollments.views import *
from apps.feedback.views import *
from apps.suggestions.views import *
from apps.users.views import *

from django.conf import settings
from django.conf.urls.static import static

def terms(request):
    return render(request, 'core/terms.html')
    
urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('login/', custom_login, name='login'),
    path('logout/', custom_logout, name='logout'),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('profile/edit/', profile_edit, name='profile_edit'),
    path('profile_pro/', profile_pro, name='profile_pro'),
    path('profile_pro/edit/', profile_pro_edit, name='profile_pro_edit'),
    path('become-instructor/', become_instructor, name='become_instructor'),
    path('contact/', ContactView.as_view(), name='contact'),

    path('users/', user_list, name='user_list'),
    path('users/<int:pk>/change-type/', change_user_type, name='change_user_type'),

    path('users/instructor-requests/', instructor_requests, name='instructor_requests'),
    path('users/approve-instructor/<int:user_id>/', approve_instructor, name='approve_instructor'),
    path('users/instructor_request_detail/<int:user_id>/', instructor_request_detail, name='instructor_request_detail'),


    # path('feedback/', feedback_list, name='feedback_list'),
    # path('feedback/create/', feedback_create, name='feedback_create'),
    # path('feedback/<int:pk>/update/', feedback_update, name='feedback_update'),
    # path('feedback/<int:pk>/delete/', feedback_delete, name='feedback_delete'),
    path('about/', about, name='about'),
    path('terms/', terms, name='terms'),
    
    path('', include('apps.enrollments.urls', namespace='enrollments')),
    path('', include('apps.courses.urls', namespace='courses')),
    path('', include('apps.reviews.urls', namespace='reviews')),
    path('', include('apps.feedback.urls', namespace='feedback')),
    path('', include('apps.suggestions.urls', namespace='suggestions')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
