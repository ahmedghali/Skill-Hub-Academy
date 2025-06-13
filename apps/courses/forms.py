from django import forms
from django.utils.text import slugify
from .models import Course, Category, User
from cloudinary.forms import CloudinaryFileField


##############################################################
class CourseForm(forms.ModelForm):
    # thumbnail = CloudinaryFileField(
    #     attrs={'class': 'form-control'},
    #     required=False,
    #     options={
    #         'folder': 'courses/thumbnails/',
    #         'allowed_formats': ['jpg', 'png', 'jpeg'],
    #     }
    # )

    class Meta:
        model = Course
        fields = [
            'title', 'description', 'objectives', 'category', 'price', 'duration_hours',
            'max_participants', 'min_participants', 'delivery_mode', 'target_audience',
            'difficulty_level', 'prerequisites', 'required_materials', 'thumbnail',
            'intro_video', 'is_featured'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'عنوان الدورة'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'وصف الدورة'}),
            'objectives': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'أهداف الدورة'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'السعر بالدينار'}),
            'duration_hours': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'المدة بالساعات'}),
            'max_participants': forms.NumberInput(attrs={'class': 'form-control'}),
            'min_participants': forms.NumberInput(attrs={'class': 'form-control'}),
            'delivery_mode': forms.Select(attrs={'class': 'form-control'}),
            'target_audience': forms.Select(attrs={'class': 'form-control'}),
            'difficulty_level': forms.Select(attrs={'class': 'form-control'}),
            'prerequisites': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'المتطلبات الأساسية'}),
            'required_materials': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'المواد المطلوبة'}),
            'thumbnail': forms.FileInput(attrs={'class': 'form-control'}),
            'intro_video': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'رابط الفيديو التمهيدي'}),
            # 'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            # 'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'title': 'عنوان الدورة',
            'description': 'الوصف',
            'objectives': 'أهداف الدورة',
            'category': 'الفئة',
            'price': 'السعر (د.ج)',
            'duration_hours': 'المدة (ساعات)',
            'max_participants': 'الحد الأقصى للمشاركين',
            'min_participants': 'الحد الأدنى للمشاركين',
            'delivery_mode': 'طريقة التقديم',
            'target_audience': 'الجمهور المستهدف',
            'difficulty_level': 'مستوى الصعوبة',
            'prerequisites': 'المتطلبات الأساسية',
            'required_materials': 'المواد المطلوبة',
            'thumbnail': 'صورة الدورة',
            'intro_video': 'فيديو تمهيدي',
            # 'is_active': 'نشط',
            # 'is_featured': 'مميز',
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        slug = slugify(title)
        # Exclure l'instance actuelle lors de la mise à jour
        if self.instance and self.instance.pk:
            if Course.objects.filter(slug=slug).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("عنوان الدورة موجود بالفعل، يرجى اختيار عنوان آخر.")
        else:
            if Course.objects.filter(slug=slug).exists():
                raise forms.ValidationError("عنوان الدورة موجود بالفعل، يرجى اختيار عنوان آخر.")
        return title  

    def save(self, commit=True):
        course = super().save(commit=False)
        course.slug = slugify(self.cleaned_data['title'])
        if commit:
            course.save()
        return course
    
    def clean(self):
        cleaned_data = super().clean()
        min_participants = cleaned_data.get('min_participants')
        max_participants = cleaned_data.get('max_participants')
        if min_participants and max_participants and min_participants > max_participants:
            raise forms.ValidationError("الحد الأدنى للمشاركين يجب أن يكون أقل من أو يساوي الحد الأقصى.")
        return cleaned_data
    


##############################################################
class CourseFormAdmin(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            'title', 'description', 'objectives', 'category', 'price', 'duration_hours',
            'max_participants', 'min_participants', 'delivery_mode', 'target_audience',
            'difficulty_level', 'prerequisites', 'required_materials', 'thumbnail',
            'intro_video', 'is_active', 'is_featured'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'عنوان الدورة'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'وصف الدورة'}),
            'objectives': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'أهداف الدورة'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'السعر بالدينار'}),
            'duration_hours': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'المدة بالساعات'}),
            'max_participants': forms.NumberInput(attrs={'class': 'form-control'}),
            'min_participants': forms.NumberInput(attrs={'class': 'form-control'}),
            'delivery_mode': forms.Select(attrs={'class': 'form-control'}),
            'target_audience': forms.Select(attrs={'class': 'form-control'}),
            'difficulty_level': forms.Select(attrs={'class': 'form-control'}),
            'prerequisites': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'المتطلبات الأساسية'}),
            'required_materials': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'المواد المطلوبة'}),
            'thumbnail': forms.FileInput(attrs={'class': 'form-control'}),
            'intro_video': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'رابط الفيديو التمهيدي'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'title': 'عنوان الدورة',
            'description': 'الوصف',
            'objectives': 'أهداف الدورة',
            'category': 'الفئة',
            'price': 'السعر (د.ج)',
            'duration_hours': 'المدة (ساعات)',
            'max_participants': 'الحد الأقصى للمشاركين',
            'min_participants': 'الحد الأدنى للمشاركين',
            'delivery_mode': 'طريقة التقديم',
            'target_audience': 'الجمهور المستهدف',
            'difficulty_level': 'مستوى الصعوبة',
            'prerequisites': 'المتطلبات الأساسية',
            'required_materials': 'المواد المطلوبة',
            'thumbnail': 'صورة الدورة',
            'intro_video': 'فيديو تمهيدي',
            'is_active': 'نشط',
            'is_featured': 'مميز',
        }

    


    def clean_title(self):
        title = self.cleaned_data.get('title')
        slug = slugify(title)
        # Exclure l'instance actuelle lors de la mise à jour
        if self.instance and self.instance.pk:
            if Course.objects.filter(slug=slug).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("عنوان الدورة موجود بالفعل، يرجى اختيار عنوان آخر.")
        else:
            if Course.objects.filter(slug=slug).exists():
                raise forms.ValidationError("عنوان الدورة موجود بالفعل، يرجى اختيار عنوان آخر.")
        return title
    
    

    def save(self, commit=True):
        course = super().save(commit=False)
        course.slug = slugify(self.cleaned_data['title'])
        if commit:
            course.save()
        return course
    
    def clean(self):
        cleaned_data = super().clean()
        min_participants = cleaned_data.get('min_participants')
        max_participants = cleaned_data.get('max_participants')
        if min_participants and max_participants and min_participants > max_participants:
            raise forms.ValidationError("الحد الأدنى للمشاركين يجب أن يكون أقل من أو يساوي الحد الأقصى.")
        return cleaned_data
    
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['instructor'].queryset = User.objects.filter(user_type='instructor')
    

# apps/courses/forms.py
from django import forms
from .models import CourseSession

class CourseSessionForm(forms.ModelForm):
    class Meta:
        model = CourseSession
        fields = ['start_date', 'end_date', 'location', 'meeting_link']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'مكان الجلسة'}),
            'meeting_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'رابط الاجتماع'}),
        }
        labels = {
            'start_date': 'تاريخ البدء',
            'end_date': 'تاريخ الانتهاء',
            'location': 'المكان',
            'meeting_link': 'رابط الاجتماع',
        }



from django import forms
from .models import Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'اسم الفئة'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'وصف الفئة'}),
        }
        labels = {
            'name': 'اسم الفئة',
            'description': 'وصف الفئة',
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if Category.objects.filter(name=name).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise forms.ValidationError('فئة بهذا الاسم موجودة بالفعل.')
        return name




from django import forms
from .models import Project, Course

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['course', 'title', 'description', 'resources', 'order']
        widgets = {
            'course': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'عنوان المشروع'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'وصف المشروع'}),
            'resources': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'رابط المصادر'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'ترتيب المشروع'}),
        }
        labels = {
            'course': 'الدورة',
            'title': 'العنوان',
            'description': 'الوصف',
            'resources': 'المصادر',
            'order': 'الترتيب',
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and user.user_type == 'instructor':
            self.fields['course'].queryset = Course.objects.filter(instructor=user)




# from django import forms
# from .models import InstructorApplication

# class InstructorApplicationForm(forms.ModelForm):
#     class Meta:
#         model = InstructorApplication
#         fields = ['bio', 'experience', 'certificate']
#         widgets = {
#             'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
#             'experience': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
#             'certificate': forms.FileInput(attrs={'class': 'form-control'}),
#         }