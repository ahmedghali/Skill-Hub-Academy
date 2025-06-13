from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Enrollment
from apps.courses.models import Course, CourseSession
from django.utils import timezone

@login_required
def enroll(request, course_pk):
    if request.user.user_type != 'student':
        messages.error(request, 'التسجيل متاح للطلاب فقط.')
        return redirect('courses:course_detail', pk=course_pk)
    course = get_object_or_404(Course, pk=course_pk, is_active=True)
    if request.method == 'POST':
        session_pk = request.POST.get('session_pk')
        session = get_object_or_404(CourseSession, pk=session_pk, course=course, is_cancelled=False)
        if session.current_participants >= course.max_participants:
            messages.error(request, 'الجلسة مكتملة.')
            return redirect('courses:course_detail', pk=course_pk)
        enrollment, created = Enrollment.objects.get_or_create(
            student=request.user, session=session, defaults={'course': course, 'is_active': True, 'status': 'pending'}
        )
        if created:
            session.current_participants += 1
            session.save()
            messages.success(request, 'تم التسجيل في الدورة بنجاح! في انتظار التأكيد.')
        else:
            messages.info(request, 'أنت مسجل بالفعل في هذه الجلسة.')
        return redirect('enrollments:enrollment_list')
    return redirect('courses:course_detail', pk=course_pk)

@login_required
def enrollment_list(request):
    if request.user.user_type != 'student':
        messages.error(request, 'هذه الصفحة متاحة للطلاب فقط.')
        return redirect('profile')
    enrollments = Enrollment.objects.filter(student=request.user, is_active=True)
    context = {'enrollments': enrollments}
    return render(request, 'enrollments/enrollment_list.html', context)



@login_required
def enrollment_update(request, pk):
    enrollment = get_object_or_404(Enrollment, pk=pk, student=request.user)
    if request.user.user_type != 'student':
        messages.error(request, 'لا يمكنك تعديل هذا التسجيل.')
        return redirect('profile')
    if enrollment.status != 'pending':
        messages.error(request, 'لا يمكن تعديل التسجيل بعد تغيير حالته من قبل المشرف.')
        return redirect('profile')
    elif request.method == 'POST':
            session_pk = request.POST.get('session_pk')
            session = get_object_or_404(CourseSession, pk=session_pk, course=enrollment.course, is_cancelled=False)
            if session.current_participants >= enrollment.course.max_participants and session != enrollment.session:
                messages.error(request, 'الجلسة المختارة مكتملة.')
                return redirect('enrollments:enrollment_list')
            # Mettre à jour l'ancienne session
            if enrollment.session != session:
                if enrollment.session.current_participants > 0:
                    enrollment.session.current_participants -= 1
                    enrollment.session.save()
                # Mettre à jour la nouvelle session
                session.current_participants += 1
                session.save()
                enrollment.session = session
                enrollment.status = 'pending'  # Réinitialiser le statut
                enrollment.save()
                messages.success(request, 'تم تعديل التسجيل بنجاح!')
                return redirect('enrollments:enrollment_list')
    sessions = enrollment.course.sessions_course.filter(is_cancelled=False)
    context = {'enrollment': enrollment, 'sessions': sessions}
    return render(request, 'enrollments/enrollment_update.html', context)

@login_required
def enrollment_cancel(request, pk):
    enrollment = get_object_or_404(Enrollment, pk=pk, student=request.user)
    if request.user.user_type != 'student':
        messages.error(request, 'لا يمكنك إلغاء هذا التسجيل.')
        return redirect('profile')
    if request.method == 'POST':
        enrollment.is_active = False
        enrollment.status = 'cancelled'
        if enrollment.session.current_participants > 0:
            enrollment.session.current_participants -= 1
            enrollment.session.save()
        enrollment.save()
        messages.success(request, 'تم إلغاء التسجيل بنجاح!')
        return redirect('enrollments:enrollment_list')
    return render(request, 'enrollments/enrollment_cancel.html', {'enrollment': enrollment})



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Enrollment
from .forms import EnrollmentAdminForm

@login_required
def enrollment_list_admin(request):
    if request.user.user_type != 'admin':
        return HttpResponseForbidden("ليس لديك صلاحية لعرض التسجيلات.")
    enrollments = Enrollment.objects.all().order_by('-enrolled_at')
    return render(request, 'enrollments/enrollment_list_admin.html', {'enrollments': enrollments})

@login_required
def enrollment_update_admin(request, pk):
    if request.user.user_type != 'admin':
        return HttpResponseForbidden("ليس لديك صلاحية لتعديل التسجيلات.")
    enrollment = get_object_or_404(Enrollment, pk=pk)
    if request.method == 'POST':
        form = EnrollmentAdminForm(request.POST, instance=enrollment)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تحديث حالة التسجيل بنجاح!')
            return redirect('enrollments:enrollment_list_admin')
        else:
            messages.error(request, 'يرجى تصحيح الأخطاء أدناه.')
    else:
        form = EnrollmentAdminForm(instance=enrollment)
    return render(request, 'enrollments/enrollment_form_admin.html', {'form': form, 'enrollment': enrollment})



@login_required
def enrollment_delete(request, pk):
    enrollment = get_object_or_404(Enrollment, pk=pk, student=request.user)
    if enrollment.status != 'pending':
        messages.error(request, 'لا يمكن حذف التسجيل بعد تغيير حالته من قبل المشرف.')
        return redirect('profile')
    if request.method == 'POST':
        enrollment.delete()
        messages.success(request, 'تم حذف التسجيل بنجاح!')
        return redirect('profile')
    return render(request, 'enrollments/enrollment_confirm_delete.html', {'enrollment': enrollment})