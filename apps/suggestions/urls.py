from django.urls import path
from .views import *

app_name = 'suggestions'

urlpatterns = [
    path('suggestions/', suggestion_list, name='suggestion_list'),
    path('suggestions/create/', suggestion_create, name='suggestion_create'),
    path('suggestions/<int:pk>/update/', suggestion_update, name='suggestion_update'),
    path('suggestions/<int:pk>/delete/', suggestion_delete, name='suggestion_delete'),
    path('suggestions/<int:pk>/admin-response/', suggestion_admin_response, name='suggestion_admin_response'),
    path('suggestions/admin/', admin_suggestion_list, name='admin_suggestion_list'),
]

