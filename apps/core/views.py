from django.shortcuts import render
from apps.courses.models import Course, Category
from apps.reviews.models import Review
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages


def home(request):
    featured_courses = Course.objects.filter(is_active=True, is_featured=True)[:6]
    categories = Category.objects.all()[:6]  # Limiter à 6 catégories
    recent_reviews = Review.objects.filter(is_active=True).order_by('-created_at')[:6]
    context = {
        'featured_courses': featured_courses,
        'categories': categories,
        'recent_reviews': recent_reviews,
    }
    return render(request, 'core/home.html', context)



class ContactView(View):
    def get(self, request):
        return render(request, 'core/contact.html')

    def post(self, request):
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        if subject and message:
            messages.success(request, 'تم إرسال رسالتك بنجاح!')
            print("Message de contact ajouté: تم إرسال رسالتك بنجاح.")  # Débogage
        else:
            messages.error(request, 'يرجى ملء جميع الحقول.')
            print("Erreur de contact: champs manquants")  # Débogage
        return redirect('home')
    

def about(request):
    return render(request, 'core/about.html')