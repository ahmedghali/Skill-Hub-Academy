# apps/reviews/models.py
from django.db import models
from django.contrib.auth import get_user_model
from apps.courses.models import Course
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()

class Review(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews', verbose_name='الدورة')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_given', verbose_name='الطالب')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name='التقييم')
    comment = models.TextField(blank=True, verbose_name='التعليق')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تم إنشاؤها في')
    is_active = models.BooleanField(default=False, verbose_name='نشط')
    
    class Meta:
        verbose_name_plural = "المراجعات"
        unique_together = ['course', 'student']
    
    def __str__(self):
        return f"{self.course.title} - {self.rating}★"