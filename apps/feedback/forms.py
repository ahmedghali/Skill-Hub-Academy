from django import forms
from .models import GeneralFeedback

class GeneralFeedbackForm(forms.ModelForm):
    class Meta:
        model = GeneralFeedback
        fields = ['feedback_type', 'subject', 'message']
        widgets = {
            'feedback_type': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'الموضوع'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'اكتب تعليقك هنا'}),
        }
        labels = {
            'feedback_type': 'نوع التعليق',
            'subject': 'الموضوع',
            'message': 'الرسالة',
        }

class AdminFeedbackResponseForm(forms.ModelForm):
    class Meta:
        model = GeneralFeedback
        fields = ['is_validated', 'is_resolved', 'admin_response']
        widgets = {
            'is_validated': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_resolved': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'admin_response': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'اكتب ردك هنا'}),
        }
        labels = {
            'is_validated': 'تم التحقق',
            'is_resolved': 'تم حلها',
            'admin_response': 'رد المشرف',
        }



