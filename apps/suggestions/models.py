# apps/feedback/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.
##########################################################################
class CourseSuggestion(models.Model):
    SUGGESTION_TYPES = [
        ('general', 'التدريب العام'),
        ('custom', 'تدريب مخصص حسب الطلب'),
        ('private', 'التدريب الفردي'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'قيد الإنتظار'),
        ('reviewing', 'قيد المراجعة'),
        ('approved', 'تمت الموافقة'),
        ('rejected', 'مرفوض'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='suggestions_user', verbose_name='المستخدم')
    title = models.CharField(max_length=200, verbose_name='العنوان')
    description = models.TextField(verbose_name='الوصف')
    suggestion_type = models.CharField(max_length=20, choices=SUGGESTION_TYPES, verbose_name='نوع الاقتراح')
    target_audience = models.CharField(max_length=50, blank=True, verbose_name='الجمهور المستهدف')
    estimated_duration = models.PositiveIntegerField(null=True, blank=True, help_text="المدة المقدرة بالساعات", verbose_name='المدة المقدَّرة')
    max_participants = models.PositiveIntegerField(null=True, blank=True, verbose_name='الحد الأقصى للمشاركين')
    budget_range = models.CharField(max_length=100, blank=True, verbose_name='نطاق الميزانية')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='الحالة')
    admin_notes = models.TextField(blank=True, verbose_name='ملاحظات المشرف')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تم إنشاؤها في')

    class Meta:
        verbose_name_plural = "اقتراح دورة تدريبية"
    
    def __str__(self):
        return f"Suggestion: {self.title} par {self.user.username}"
