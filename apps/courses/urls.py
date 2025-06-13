from django.urls import path
from .views import category_create, category_delete, category_update, course_list, course_create, course_list_admin, course_update, course_delete, course_detail, course_session_create, course_session_update, course_session_delete, category_list, category_detail, course_update_admin, project_create, project_delete, project_list, project_update

app_name = 'courses'

urlpatterns = [
    path('courses/', course_list, name='course_list'),
    path('courses/create/', course_create, name='course_create'),
    path('courses/<int:pk>/', course_detail, name='course_detail'),
    path('courses/<int:pk>/update/', course_update, name='course_update'),
    path('courses/<int:pk>/delete/', course_delete, name='course_delete'),

    path('courses/<int:course_pk>/sessions/add/', course_session_create, name='course_session_create'),
    path('courses/<int:course_pk>/sessions/<int:session_pk>/update/', course_session_update, name='course_session_update'),
    path('courses/<int:course_pk>/sessions/<int:session_pk>/delete/', course_session_delete, name='course_session_delete'),
    
    path('courses/admin/', course_list_admin, name='course_list_admin'),
    path('courses/admin/<slug:slug>/update/', course_update_admin, name='course_update_admin'),

    path('categories/', category_list, name='category_list'),
    path('categories/create/', category_create, name='category_create'),
    path('categories/<slug:slug>/', category_detail, name='category_detail'),
    path('categories/<slug:slug>/update/', category_update, name='category_update'),
    path('categories/<slug:slug>/delete/', category_delete, name='category_delete'),

    path('projects/', project_list, name='project_list'),
    path('projects/create/', project_create, name='project_create'),
    path('projects/<int:pk>/update/', project_update, name='project_update'),
    path('projects/<int:pk>/delete/', project_delete, name='project_delete'),
    
]