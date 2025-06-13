from django.http import HttpResponseForbidden
from django.shortcuts import render
from apps.feedback.models import GeneralFeedback
from apps.feedback.forms import AdminFeedbackResponseForm, GeneralFeedbackForm  # À créer
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.feedback.models import GeneralFeedback
from django.contrib import messages

# def feedback_list(request):
#     feedbacks = GeneralFeedback.objects.all()
#     context = {'feedbacks': feedbacks}
#     return render(request, 'feedback/feedback_list.html', context)


def feedback_list(request):
    if request.user.is_authenticated and request.user.user_type == 'admin':
        feedbacks = GeneralFeedback.objects.all().order_by('-created_at')
    else:
        feedbacks = GeneralFeedback.objects.filter(is_validated=True).order_by('-created_at')
    return render(request, 'feedback/feedback_list.html', {'feedbacks': feedbacks})



@login_required
def feedback_create(request):
    if request.method == 'POST':
        form = GeneralFeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            messages.success(request, 'تم إرسال التعليق بنجاح! سيتم عرضه بعد التحقق.')
            return redirect('feedback:feedback_list')
        else:
            messages.error(request, 'يرجى تصحيح الأخطاء أدناه.')
    else:
        form = GeneralFeedbackForm()
    return render(request, 'feedback/feedback_form.html', {'form': form, 'title': 'إضافة تعليق جديد'})



def feedback_update(request, pk):
    feedback = get_object_or_404(GeneralFeedback, pk=pk, user=request.user)
    if feedback.is_validated:
        messages.error(request, 'لا يمكن تعديل التعليق بعد التحقق من قبل المشرف.')
        return redirect('profile')
    if request.method == 'POST':
        form = GeneralFeedbackForm(request.POST, instance=feedback)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تعديل التعليق بنجاح!')
            return redirect('profile')
        else:
            messages.error(request, 'يرجى تصحيح الأخطاء أدناه.')
    else:
        form = GeneralFeedbackForm(instance=feedback)
    return render(request, 'feedback/feedback_form.html', {'form': form, 'title': 'تعديل التعليق'})




@login_required
def feedback_delete(request, pk):
    feedback = get_object_or_404(GeneralFeedback, pk=pk, user=request.user)
    if feedback.is_validated:
        messages.error(request, 'لا يمكن حذف التعليق بعد التحقق من avant المشرف.')
        return redirect('profile')
    if request.method == 'POST':
        feedback.delete()
        messages.success(request, 'تم حذف التعليق بنجاح!')
        return redirect('profile')
    return render(request, 'feedback/feedback_confirm_delete.html', {'feedback': feedback})





@login_required
def feedback_admin_response(request, pk):
    if request.user.user_type != 'admin':
        return HttpResponseForbidden("ليس لديك صلاحية للرد على التعليقات.")
    feedback = get_object_or_404(GeneralFeedback, pk=pk)
    if request.method == 'POST':
        form = AdminFeedbackResponseForm(request.POST, instance=feedback)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تحديث التعليق بنجاح!')
            return redirect('feedback:feedback_list')
        else:
            messages.error(request, 'يرجى تصحيح الأخطاء أدناه.')
    else:
        form = AdminFeedbackResponseForm(instance=feedback)
    return render(request, 'feedback/admin_feedback_response.html', {'form': form, 'feedback': feedback, 'title': 'الرد على التعليق'})



from django.shortcuts import render, get_object_or_404
from .models import GeneralFeedback

@login_required
def feedback_detail(request, pk):
    feedback = get_object_or_404(GeneralFeedback, pk=pk, user=request.user)
    return render(request, 'feedback/feedback_detail.html', {'feedback': feedback})