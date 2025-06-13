# apps/users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from cloudinary.models import CloudinaryField


##########################################################################
class User(AbstractUser):
    USER_TYPES = [
        ('student', 'طالب'),
        ('instructor', 'مدرس'),
        ('admin', 'إدارة'),
    ]
    
    is_instructor_pending = models.BooleanField(default=False)
    is_admin_pending = models.BooleanField(default=False)
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='student', verbose_name='نوع المستخدم')
    phone = models.CharField(max_length=20, blank=True, verbose_name='الهاتف')
    email = models.EmailField(blank=True, verbose_name='البريد الإلكتروني')
    address = models.CharField(max_length=200, blank=True, verbose_name='العنوان')
    bio = models.TextField(blank=True, verbose_name='السيرة الذاتية')
    profile_image = CloudinaryField('image', blank=True, null=True)  # URL Cloudinary
    date_of_birth = models.DateField(null=True, blank=True, verbose_name='تاريخ الميلاد')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تم إنشاؤه في')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تم التحديث في')

    class Meta:
        verbose_name_plural = "المستخدمين"

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"



##########################################################################
class InstructorProfile(models.Model):
    EXPERIENCE_LEVELS = [
        ('junior', 'Junior (1-2 ans)'),
        ('intermediate', 'Intermédiaire (3-5 ans)'),
        ('senior', 'Senior (5-10 ans)'),
        ('expert', 'Expert (10+ ans)'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='instructor_profile', verbose_name='المستخدم')
    specializations = models.TextField(help_text="التخصصات مفصولة بفواصل", verbose_name='الاختصاصات')
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_LEVELS, verbose_name='مستوى الخبرة')
    certification = models.TextField(blank=True, verbose_name='الشهادة')
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, verbose_name='أجر الساعة (د.ج)')
    is_verified = models.BooleanField(default=False, verbose_name='تم التحقق منه')

    class Meta:
        verbose_name_plural = "الملف الشخصي للمدرب"
    
    def __str__(self):
        return f"Formateur: {self.user.get_full_name()}"