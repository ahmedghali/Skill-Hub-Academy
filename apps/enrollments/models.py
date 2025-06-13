# apps/enrollments/models.py
from django.db import models
from django.contrib.auth import get_user_model
from apps.courses.models import Course, CourseSession

User = get_user_model()



##########################################################################
class Enrollment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'في الإنتظار'),
        ('confirmed', 'تم التأكيد'),
        ('completed', 'مكتمل'),
        ('cancelled', 'تم الإلغاء'),
    ]
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments_student', verbose_name='الطالب')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments_course', verbose_name='الدورة')
    session = models.ForeignKey(CourseSession, on_delete=models.CASCADE, related_name='enrollments_session', verbose_name='الجلسة')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='الحالة')
    enrolled_at = models.DateTimeField(auto_now_add=True, verbose_name='مسجّل في')
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='اكتمل في')
    is_active = models.BooleanField(default=True, verbose_name='نشط')
    
    class Meta:
        verbose_name_plural = "التسجيلات"
        unique_together = ['student', 'session']
    
    def __str__(self):
        return f"{self.student.username} - {self.course.title}"