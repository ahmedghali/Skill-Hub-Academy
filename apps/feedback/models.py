# apps/feedback/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()






##########################################################################
class GeneralFeedback(models.Model):
    FEEDBACK_TYPES = [
        ('suggestion', 'اقتراح'),
        ('complaint', 'شكوى'),
        ('compliment', 'شكر'),
        ('bug_report', 'تبليغ عن خطأ'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedback_user', verbose_name='المستخدم')
    feedback_type = models.CharField(max_length=20, choices=FEEDBACK_TYPES, verbose_name='نوع التعليقات')
    subject = models.CharField(max_length=200, verbose_name='الموضوع')
    message = models.TextField(verbose_name='الرسالة')
    is_resolved = models.BooleanField(default=False, verbose_name='تم حلها')
    is_validated = models.BooleanField(default=False, verbose_name='تم التحقق')  # Nouveau champ
    admin_response = models.TextField(blank=True, verbose_name='رد المشرف')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تم إنشاؤها في')

    class Meta:
        verbose_name_plural = "التعليقات العامة"
    
    def __str__(self):
        return f"{self.get_feedback_type_display()}: {self.subject}"