from django import forms
from .models import CourseSuggestion

class CourseSuggestionForm(forms.ModelForm):
    class Meta:
        model = CourseSuggestion
        fields = ['title', 'description', 'suggestion_type', 'target_audience', 'estimated_duration', 'max_participants', 'budget_range']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'عنوان الاقتراح'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'وصف الاقتراح'}),
            'suggestion_type': forms.Select(attrs={'class': 'form-control'}),
            'target_audience': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'الجمهور المستهدف'}),
            'estimated_duration': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'المدة بالساعات'}),
            'max_participants': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'الحد الأقصى للمشاركين'}),
            'budget_range': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نطاق الميزانية'}),
        }
        labels = {
            'title': 'العنوان',
            'description': 'الوصف',
            'suggestion_type': 'نوع الاقتراح',
            'target_audience': 'الجمهور المستهدف',
            'estimated_duration': 'المدة المقدرة (ساعات)',
            'max_participants': 'الحد الأقصى للمشاركين',
            'budget_range': 'نطاق الميزانية',
        }

class AdminSuggestionResponseForm(forms.ModelForm):
    class Meta:
        model = CourseSuggestion
        fields = ['status', 'admin_notes']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'admin_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'اكتب ملاحظاتك هنا'}),
        }
        labels = {
            'status': 'الحالة',
            'admin_notes': 'ملاحظات المشرف',
        }