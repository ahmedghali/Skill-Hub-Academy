
from django import forms
from .models import Review, Course

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, f"{i} ★") for i in range(1, 6)], attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'اكتب تعليقك هنا'}),
        }
        labels = {
            'rating': 'التقييم',
            'comment': 'التعليق',
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.course = kwargs.pop('course', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        if self.user and self.course:
            if Review.objects.filter(student=self.user, course=self.course).exclude(pk=self.instance.pk if self.instance else None).exists():
                raise forms.ValidationError('لقد قمت بالفعل بتقييم هذه الدورة.')
        return cleaned_data