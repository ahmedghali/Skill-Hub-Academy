from django.urls import path
from .views import enroll, enrollment_delete, enrollment_list, enrollment_list_admin, enrollment_update, enrollment_cancel, enrollment_update_admin

app_name = 'enrollments'

urlpatterns = [
    path('courses/<int:course_pk>/enroll/', enroll, name='enroll'),
    path('enrollments/', enrollment_list, name='enrollment_list'),
    path('enrollments/<int:pk>/update/', enrollment_update, name='enrollment_update'),
    path('enrollments/<int:pk>/cancel/', enrollment_cancel, name='enrollment_cancel'),
    path('enrollments/admin/', enrollment_list_admin, name='enrollment_list_admin'),
    path('enrollments/admin/<int:pk>/update/', enrollment_update_admin, name='enrollment_update_admin'),
    path('enrollments/<int:pk>/delete/', enrollment_delete, name='enrollment_delete'),
    
]