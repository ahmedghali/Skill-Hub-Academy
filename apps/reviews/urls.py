
from django.urls import path
from apps.reviews.views import review_delete, review_update, review_create


app_name = 'reviews'

urlpatterns = [
    path('reviews/<slug:course_slug>/create/', review_create, name='review_create'),
    path('reviews/<int:pk>/update/', review_update, name='review_update'),
    path('reviews/<int:pk>/delete/', review_delete, name='review_delete'),
    
]

    