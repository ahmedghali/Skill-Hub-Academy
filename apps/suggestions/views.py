from django.http import HttpResponseForbidden
from django.shortcuts import render
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CourseSuggestion
from .forms import CourseSuggestionForm, AdminSuggestionResponseForm




def suggestion_list(request):
    if request.user.is_authenticated and request.user.user_type == 'admin':
        suggestions = CourseSuggestion.objects.all().order_by('-created_at')
    else:
        suggestions = CourseSuggestion.objects.filter(user=request.user.id).order_by('-created_at')
    return render(request, 'suggestions/suggestion_list.html', {'suggestions': suggestions})




@login_required
def suggestion_create(request):
    if request.method == 'POST':
        form = CourseSuggestionForm(request.POST)
        if form.is_valid():
            suggestion = form.save(commit=False)
            suggestion.user = request.user
            suggestion.save()
            messages.success(request, 'تم إرسال اقتراح الدورة بنجاح!')
            return redirect('suggestions:suggestion_list')
        else:
            messages.error(request, 'يرجى تصحيح الأخطاء أدناه.')
    else:
        form = CourseSuggestionForm()
    return render(request, 'suggestions/suggestion_form.html', {'form': form, 'title': 'إضافة اقتراح دورة'})



@login_required
def suggestion_update(request, pk):
    suggestion = get_object_or_404(CourseSuggestion, pk=pk, user=request.user)
    if suggestion.status != 'pending':
        messages.error(request, 'لا يمكن تعديل الاقتراح بعد تغيير حالته من قبل المشرف.')
        return redirect('profile')
    if request.method == 'POST':
        form = CourseSuggestionForm(request.POST, instance=suggestion)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تعديل الاقتراح بنجاح!')
            return redirect('profile')
        else:
            messages.error(request, 'يرجى تصحيح الأخطاء أدناه.')
    else:
        form = CourseSuggestionForm(instance=suggestion)
    return render(request, 'suggestions/suggestion_form.html', {'form': form, 'title': 'تعديل اقتراح دورة'})

@login_required
def suggestion_delete(request, pk):
    suggestion = get_object_or_404(CourseSuggestion, pk=pk, user=request.user)
    if suggestion.status != 'pending':
        messages.error(request, 'لا يمكن حذف الاقتراح بعد تغيير حالته من قبل المشرف.')
        return redirect('profile')
    if request.method == 'POST':
        suggestion.delete()
        messages.success(request, 'تم حذف الاقتراح بنجاح!')
        return redirect('profile')
    return render(request, 'suggestions/suggestion_confirm_delete.html', {'suggestion': suggestion})



@login_required
def suggestion_admin_response(request, pk):
    if request.user.user_type != 'admin':
        return HttpResponseForbidden("ليس لديك صلاحية للرد على الاقتراحات.")
    suggestion = get_object_or_404(CourseSuggestion, pk=pk)
    if request.method == 'POST':
        form = AdminSuggestionResponseForm(request.POST, instance=suggestion)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تحديث الاقتراح بنجاح!')
            return redirect('suggestions:suggestion_list')
        else:
            messages.error(request, 'يرجى تصحيح الأخطاء أدناه.')
    else:
        form = AdminSuggestionResponseForm(instance=suggestion)
    return render(request, 'suggestions/admin_suggestion_response.html', {'form': form, 'suggestion': suggestion, 'title': 'الرد على اقتراح الدورة'})



@login_required
def admin_suggestion_list(request):
    if request.user.user_type != 'admin':
        return HttpResponseForbidden("ليس لديك صلاحية لعرض الاقتراحات.")
    suggestions = CourseSuggestion.objects.all().order_by('-created_at')
    return render(request, 'suggestions/admin_suggestion_list.html', {'suggestions': suggestions})