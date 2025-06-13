from django import forms
from django.contrib.auth.forms import UserCreationForm
from apps.users.models import User
from cloudinary.forms import CloudinaryFileField
from .models import User, InstructorProfile

class UserRegisterForm(UserCreationForm):
    # user_type = forms.ChoiceField(choices=User.USER_TYPES, label="نوع المستخدم")
    phone = forms.CharField(max_length=20, required=False, label="الهاتف")
    bio = forms.CharField(widget=forms.Textarea, required=False, label="السيرة الذاتية")
    profile_image = CloudinaryFileField(
        required=False,
        label="صورة الملف الشخصي",
        widget=forms.FileInput(attrs={'class': 'form-control'}),  # Utiliser widget au lieu de attrs
        options={'folder': 'users/profiles/', 'allowed_formats': ['jpg', 'png', 'jpeg']}
    )
    date_of_birth = forms.DateField(
        required=False,
        label="تاريخ الميلاد",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'phone', 'bio', 'profile_image', 'date_of_birth']
        help_texts = {  # Supprimer les help texts
            'username': None,
            'email': None,
            'password1': None,
            'password2': None,
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class ChangeUserTypeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['user_type']
        labels = {'user_type': 'نوع المستخدم'}
        widgets = {'user_type': forms.Select(attrs={'class': 'form-control'})}


class UserProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        required=False,
        label="تاريخ الميلاد",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'address', 'bio', 'date_of_birth', 'profile_image']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'profile_image': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'username': 'اسم المستخدم',
            'email': 'البريد الإلكتروني',
            'phone': 'رقم الهاتف',
            'bio': 'السيرة الذاتية',
            'address': 'العنوان',
            'date_of_birth': 'تاريخ الميلاد',
            'profile_image': 'صورة الملف الشخصي',
        }
        help_texts = {  # Supprimer les help texts
            'username': None,
        }
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }
        def clean_profile_image(self):
            picture = self.cleaned_data.get('profile_image')
            if picture:
                if not picture.name.lower().endswith(('.jpg', '.jpeg', '.png')):
                    raise forms.ValidationError('يرجى تحميل صورة بصيغة JPG أو PNG.')
            return picture



class InstructorProfileForm(forms.ModelForm):
    class Meta:
        model = InstructorProfile
        fields = ['specializations', 'experience_level', 'certification', 'hourly_rate']
        widgets = {
            'specializations': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'experience_level': forms.Select(attrs={'class': 'form-control'}),
            'certification': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'hourly_rate': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'specializations': 'التخصصات',
            'experience_level': 'مستوى الخبرة',
            'certification': 'الشهادات',
            'hourly_rate': 'أجر الساعة (د.ج)',
        }
        
        def clean_hourly_rate(self):
            rate = self.cleaned_data.get('hourly_rate')
            if rate and rate < 0:
                raise forms.ValidationError("أجر الساعة يجب أن يكون إيجابيًا.")
            return rate
        



from django import forms
from .models import User, InstructorProfile

class BecomeInstructorForm(forms.Form):
    specializations = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}), label='التخصصات')
    experience_level = forms.ChoiceField(choices=InstructorProfile.EXPERIENCE_LEVELS, widget=forms.Select(attrs={'class': 'form-control'}), label='مستوى الخبرة')
    certification = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), required=False, label='الشهادات')
    hourly_rate = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control'}), label='أجر الساعة (د.ج)')