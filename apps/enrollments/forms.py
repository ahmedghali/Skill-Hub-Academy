from django import forms
from .models import Enrollment

class EnrollmentAdminForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'status': 'الحالة',
        }