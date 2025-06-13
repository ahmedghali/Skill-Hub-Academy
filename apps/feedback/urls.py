from django.urls import path
from .views import *

app_name = 'feedback'

urlpatterns = [
    path('feedback/', feedback_list, name='feedback_list'),
    path('feedback/create/', feedback_create, name='feedback_create'),
    path('feedback/<int:pk>/admin-response/', feedback_admin_response, name='feedback_admin_response'),
    path('feedback/<int:pk>/update/', feedback_update, name='feedback_update'),
    path('feedback/<int:pk>/delete/', feedback_delete, name='feedback_delete'),
    path('feedback/<int:pk>/', feedback_detail, name='feedback_detail'),

    # path('suggestions/', suggestion_list, name='suggestion_list'),
    # path('suggestions/create/', suggestion_create, name='suggestion_create'),
    # path('suggestions/<int:pk>/update/', suggestion_update, name='suggestion_update'),
    # path('suggestions/<int:pk>/delete/', suggestion_delete, name='suggestion_delete'),
    # path('suggestions/<int:pk>/admin-response/', suggestion_admin_response, name='suggestion_admin_response'),
]

