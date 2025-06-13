# apps/courses/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from cloudinary.models import CloudinaryField
from django.utils.text import slugify

User = get_user_model()



##########################################################################
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='اسم الفئة')
    slug = models.SlugField(max_length=100, unique=True, verbose_name="الرابط")
    description = models.TextField(blank=True, verbose_name='وصف الفئة')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تم إنشاء الفئة في')
    
    class Meta:
        verbose_name = "الفئة"
        verbose_name_plural = "الفئات"
        ordering = ['name']

    def __str__(self):
        return self.name

    # def can_delete(self):
    #     """Vérifie si la catégorie peut être supprimée (aucun cours associé)."""
    #     return not self.course_set.exists()
    @property
    def can_delete(self):
        return self.courses_category.count() == 0  # Example: True if no related courses

    def generate_unique_slug(self):
        """
        Génère un slug unique basé sur le nom, avec gestion des doublons.
        """
        # Fonction de translittération simple pour l'arabe
        transliteration_map = {
            'ا': 'a', 'أ': 'a', 'إ': 'i', 'آ': 'a',
            'ب': 'b', 'ت': 't', 'ث': 'th', 'ج': 'j',
            'ح': 'h', 'خ': 'kh', 'د': 'd', 'ذ': 'dh',
            'ر': 'r', 'ز': 'z', 'س': 's', 'ش': 'sh',
            'ص': 's', 'ض': 'd', 'ط': 't', 'ظ': 'z',
            'ع': 'a', 'غ': 'gh', 'ف': 'f', 'ق': 'q',
            'ك': 'k', 'ل': 'l', 'م': 'm', 'ن': 'n',
            'ه': 'h', 'و': 'w', 'ي': 'y', 'ى': 'y',
            'ة': 'h',
        }

        # Translittérer le nom
        slug_base = ''
        for char in self.name:
            slug_base += transliteration_map.get(char, char)

        # Nettoyer et slugifier
        slug_base = slugify(slug_base, allow_unicode=False)
        if not slug_base:
            slug_base = 'category'  # Fallback si le slug est vide

        # Vérifier l'unicité
        slug = slug_base
        counter = 1
        while Category.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f"{slug_base}-{counter}"
            counter += 1

        return slug

    def save(self, *args, **kwargs):
        if not self.slug or self.name != Category.objects.get(pk=self.pk).name if self.pk else True:
            self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)

    @property
    def course_count(self):
        return self.courses_category.count()


##########################################################################
class Course(models.Model):
    DELIVERY_MODES = [
        ('online', 'على الإنترنت'),
        ('onsite', 'حضوريًا'),
        ('hybrid', 'مدمج'),
    ]
    
    TARGET_AUDIENCES = [
        ('children', 'الأطفال (6-12 سنة)'),
        ('teens', 'المراهقون (13-17 سنة)'),
        ('adults', 'البالغون (18 عاماً فأكثر)'),
        ('seniors', 'كبار السن (55 سنة فأكثر)'),
        ('enterprise', 'الشركات'),
    ]
    
    DIFFICULTY_LEVELS = [
        ('beginner', 'مبتدئ'),
        ('intermediate', 'متوسط'),
        ('advanced', 'متقدم'),
        ('expert', 'خبير'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='عنوان الدورة')
    slug = models.SlugField(max_length=100, unique=True, verbose_name="الرابط")
    description = models.TextField(verbose_name='وصف الدورة')
    objectives = models.TextField(help_text="أهداف التدريب", verbose_name='أهداف الدورة')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='فئة الدورة', related_name='courses_category')
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='مدرب الدورة', related_name='courses_taught_instructor')
    
    # Détails de la formation
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, validators=[MinValueValidator(0)], verbose_name='سعر الدورة')
    duration_hours = models.PositiveIntegerField(help_text='ساعات مدة الدورة', verbose_name="مدة الدورة بالساعات")
    max_participants = models.PositiveIntegerField(default=10, verbose_name='الحد الأقصى للمشاركين')
    min_participants = models.PositiveIntegerField(default=1, verbose_name='الحد الأدنى للمشاركين')
    delivery_mode = models.CharField(max_length=20, choices=DELIVERY_MODES, verbose_name='طريقة تقديم الدورة التدريبية')
    target_audience = models.CharField(max_length=20, choices=TARGET_AUDIENCES, verbose_name='الجمهور المستهدف للدورة')
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_LEVELS, verbose_name='مستوى صعوبة الدورة')
    
    # Prérequis et matériel
    prerequisites = models.TextField(blank=True, help_text="المستوى المطلوب", verbose_name='المستوى المطلوب')
    required_materials = models.TextField(blank=True, help_text="الأجهزة المطلوبة", verbose_name='الأجهزة المطلوبة')
    
    # Médias

    thumbnail = CloudinaryField('image', null=True, blank=True)
    intro_video = models.URLField(blank=True, verbose_name='فيديو تمهيدي')  # URL Cloudinary/YouTube
    
    # Métadonnées
    is_active = models.BooleanField(default=False, verbose_name='نشط')
    is_featured = models.BooleanField(default=False, verbose_name='مميز')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='أُنشئت في')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تم التحديث في')
    
    class Meta:
        verbose_name_plural = "الدورات"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    @property
    def average_rating(self):
        ratings = self.reviews.all()
        if ratings:
            return sum(r.rating for r in ratings) / len(ratings)
        return 0
    
    @property
    def enrolled_count(self):
        return self.enrollments_course.filter(is_active=True).count()



##########################################################################
class CourseSession(models.Model):
    """Sessions programmées pour une formation"""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sessions_course', verbose_name='الدورة')
    start_date = models.DateTimeField(verbose_name='تاريخ البدء')
    end_date = models.DateTimeField(verbose_name='تاريخ الانتهاء')
    location = models.CharField(max_length=200, blank=True, help_text="للحضوري", verbose_name='المكان')
    meeting_link = models.URLField(blank=True, help_text="عبر الإنترنت", verbose_name='رابط اللقاء')
    current_participants = models.PositiveIntegerField(default=0, verbose_name='المشاركين الحاليين')
    is_cancelled = models.BooleanField(default=False, verbose_name='تم إلغاؤها')

    class Meta:
        verbose_name_plural = "جلسات الدورة"
    
    def __str__(self):
        return f"{self.course.title} - {self.start_date.strftime('%d/%m/%Y')}"



##########################################################################
class Project(models.Model):
    """Projets réalisés dans une formation"""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='projects_course', verbose_name='الدورة')
    title = models.CharField(max_length=200, verbose_name='العنوان')
    description = models.TextField(verbose_name='الوصف')
    resources = models.URLField(blank=True, help_text="رابط إلى المصادر", verbose_name='المصادر')
    order = models.PositiveIntegerField(default=0, verbose_name='طلب')
    
    class Meta:
        verbose_name_plural = "المشاريع"
        ordering = ['order']
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"