from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course, Review
from .forms import ReviewForm

@login_required
def review_create(request, course_slug):
    if request.user.user_type != 'student':
        return HttpResponseForbidden("يجب أن تكون طالبًا لإضافة مراجعة.")
    course = get_object_or_404(Course, slug=course_slug)
    if request.method == 'POST':
        form = ReviewForm(request.POST, user=request.user, course=course)
        if form.is_valid():
            review = form.save(commit=False)
            review.student = request.user
            review.course = course
            review.save()
            messages.success(request, 'تم إضافة المراجعة بنجاح!')
            return redirect('profile')
        else:
            messages.error(request, 'يرجى تصحيح الأخطاء أدناه.')
    else:
        form = ReviewForm()
    return render(request, 'reviews/review_form.html', {'form': form, 'title': 'إضافة مراجعة', 'course': course})

@login_required
def review_update(request, pk):
    if request.user.user_type != 'student':
        return HttpResponseForbidden("يجب أن تكون طالبًا لتعديل المراجعة.")
    review = get_object_or_404(Review, pk=pk, student=request.user)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review, user=request.user, course=review.course)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تعديل المراجعة بنجاح!')
            return redirect('profile')
        else:
            messages.error(request, 'يرجى تصحيح الأخطاء أدناه.')
    else:
        form = ReviewForm(instance=review)
    return render(request, 'reviews/review_form.html', {'form': form, 'title': 'تعديل المراجعة', 'course': review.course})

@login_required
def review_delete(request, pk):
    if request.user.user_type != 'student':
        return HttpResponseForbidden("يجب أن تكون طالبًا لحذف المراجعة.")
    review = get_object_or_404(Review, pk=pk, student=request.user)
    if request.method == 'POST':
        review.delete()
        messages.success(request, 'تم حذف المراجعة بنجاح!')
        return redirect('profile')
    return render(request, 'reviews/review_confirm_delete.html', {'review': review})