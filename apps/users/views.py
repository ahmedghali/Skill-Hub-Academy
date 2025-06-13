from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from apps.courses.models import Project
from apps.suggestions.models import CourseSuggestion
from .forms import ChangeUserTypeForm, UserRegisterForm, UserProfileForm, InstructorProfileForm, BecomeInstructorForm
from .models import User, InstructorProfile
from apps.enrollments.models import Enrollment
from apps.reviews.models import Review
from apps.feedback.models import GeneralFeedback

def is_admin(user):
    return user.is_authenticated and user.user_type == 'admin'

@login_required
@user_passes_test(is_admin)
def instructor_requests(request):
    pending_requests = User.objects.filter(is_instructor_pending=True, user_type='student')

    return render(request, 'users/instructor_requests.html', {'pending_requests': pending_requests})

@login_required
@user_passes_test(is_admin)
def instructor_request_detail(request, user_id):
    my_user = get_object_or_404(User, id=user_id, is_instructor_pending=True)
    instructor_detail = get_object_or_404(InstructorProfile, user=my_user, is_verified=False)
    return render(request, 'users/instructor_request_detail.html', {'my_user': my_user, 'instructor_detail':instructor_detail})

@login_required
@user_passes_test(is_admin)
def approve_instructor(request, user_id):
    user = get_object_or_404(User, id=user_id, is_instructor_pending=True)
    if request.method == 'POST':
        user.user_type = 'instructor'
        user.is_instructor_pending = False
        user.save()
        instructor_detail = get_object_or_404(InstructorProfile, user=user_id, is_verified=False)
        instructor_detail.is_verified = True
        instructor_detail.save()
        messages.success(request, f'{user.username} هو الآن مدرب')
        return redirect('instructor_requests')
    return render(request, 'users/approve_instructor.html', {'user': user})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'student'
            user.save()
            login(request, user)
            messages.success(request, 'تم إنشاء حسابك بنجاح!')
            return redirect('home')
        else:
            messages.error(request, 'يرجى تصحيح الأخطاء أدناه.')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})



@login_required
def change_user_type(request, pk):
    if request.user.user_type != 'admin':
        return HttpResponseForbidden("ليس لديك صلاحية لتغيير نوع المستخدم.")
    user_to_edit = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = ChangeUserTypeForm(request.POST, instance=user_to_edit)
        if form.is_valid():
            form.save()
            messages.success(request, f'تم تغيير نوع المستخدم لـ {user_to_edit.username} بنجاح!')
            return redirect('user_list')
        else:
            messages.error(request, 'يرجى تصحيح الأخطاء أدناه.')
    else:
        form = ChangeUserTypeForm(instance=user_to_edit)
    return render(request, 'users/change_user_type.html', {'form': form, 'user_to_edit': user_to_edit})

@login_required
def user_list(request):
    if request.user.user_type != 'admin':
        return HttpResponseForbidden("ليس لديك صلاحية لعرض قائمة المستخدمين.")
    users = User.objects.all().order_by('username')
    return render(request, 'users/user_list.html', {'users': users})


@login_required
def profile(request):
    enrollments = Enrollment.objects.filter(student=request.user, is_active=True)
    reviews = Review.objects.filter(student=request.user)
    suggestions = CourseSuggestion.objects.filter(user=request.user).order_by('-created_at')
    feedbacks = GeneralFeedback.objects.filter(user=request.user)
    
    context = {
        'user': request.user,
        'enrollments': enrollments,
        'reviews': reviews,
        'suggestions': suggestions,
        'feedbacks': feedbacks,
        
    }
    return render(request, 'users/profile.html', context)

@login_required
def profile_pro(request):
    if request.user.user_type != 'instructor':
        messages.error(request, 'هذا الملف مخصص للمدربين فقط.')
        return redirect('profile')
    instructor_profile = getattr(request.user, 'instructor_profile', None)
    courses_taught = request.user.courses_taught_instructor.all()
    projects = Project.objects.filter(course__instructor=request.user).order_by('order') if request.user.user_type == 'instructor' else []
    context = {
        'user': request.user,
        'instructor_profile': instructor_profile,
        'courses_taught': courses_taught,
        'projects': projects,
    }
    return render(request, 'users/profile_pro.html', context)



@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تحديث الملف الشخصي بنجاح!')
            return redirect('profile')
        else:
            messages.error(request, 'خطأ أثناء تحديث الملف الشخصي. يرجى التحقق من البيانات.')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'users/profile_edit.html', {'form': form})






@login_required
def profile_pro_edit(request):
    if request.user.user_type != 'instructor':
        messages.error(request, 'هذا الملف مخصص للمدربين فقط.')
        return redirect('profile')
    instructor_profile, created = InstructorProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = InstructorProfileForm(request.POST, instance=instructor_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تحديث الملف المهني بنجاح!')
            return redirect('profile_pro')
        else:
            messages.error(request, 'خطأ أثناء تحديث الملف المهني.')
    else:
        form = InstructorProfileForm(instance=instructor_profile)
    return render(request, 'users/profile_pro_edit.html', {'form': form})

def custom_logout(request):
    logout(request)
    messages.success(request, 'تم تسجيل خروجك بنجاح.')
    return redirect('home')

def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'مرحباً {user.username}، تم تسجيل دخولك بنجاح!')
            next_url = request.POST.get('next', reverse('profile_pro' if user.user_type == 'instructor' else 'profile'))
            try:
                return redirect(next_url)
            except:
                messages.error(request, 'خطأ في إعادة التوجيه، يتم توجيهك إلى الصفحة الرئيسية.')
                return redirect('home')
        else:
            messages.error(request, 'اسم المستخدم أو كلمة المرور غير صحيحة.')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})



# @login_required
# def become_instructor(request):
#     if request.user.user_type == 'instructor':
#         messages.info(request, 'أنت بالفعل مدرب.')
#         return redirect('profile_pro')
#     if request.method == 'POST':
#         form = BecomeInstructorForm(request.POST)
#         if form.is_valid():
#             instructor_profile, created = InstructorProfile.objects.get_or_create(user=request.user)
#             instructor_profile.specializations = form.cleaned_data['specializations']
#             instructor_profile.experience_level = form.cleaned_data['experience_level']
#             instructor_profile.certification = form.cleaned_data['certification']
#             instructor_profile.hourly_rate = form.cleaned_data['hourly_rate']
#             instructor_profile.save()
#             request.user.user_type = 'instructor'
#             request.user.save()
#             messages.success(request, 'تم تقديم طلبك لتصبح مدربًا بنجاح!')
#             return redirect('profile_pro')
#         else:
#             messages.error(request, 'خطأ أثناء تقديم الطلب.')
#     else:
#         form = BecomeInstructorForm()
#     return render(request, 'users/become_instructor.html', {'form': form})


@login_required
def become_instructor(request):
    if request.user.user_type == 'instructor':
        messages.info(request, 'أنت بالفعل مدرب.')
        return redirect('profile_pro')
    if request.user.user_type != 'student':
        messages.error(request, 'يمكن للطلاب فقط التقدم ليصبحوا مدربين')
        return redirect('home')
    if Enrollment.objects.filter(student=request.user).exists() or \
       Review.objects.filter(student=request.user).exists() or \
       GeneralFeedback.objects.filter(user=request.user).exists() or \
       CourseSuggestion.objects.filter(user=request.user).exists():
        messages.error(request, 'لديك أنشطة كطالب')
        return redirect('home')
    if request.user.is_instructor_pending:
        messages.info(request, 'طلبك قيد الانتظار')
        return redirect('home')
    if request.method == 'POST':
        form = BecomeInstructorForm(request.POST)
        if form.is_valid():
            instructor_profile, created = InstructorProfile.objects.get_or_create(user=request.user)
            instructor_profile.specializations = form.cleaned_data['specializations']
            instructor_profile.experience_level = form.cleaned_data['experience_level']
            instructor_profile.certification = form.cleaned_data['certification']
            instructor_profile.hourly_rate = form.cleaned_data['hourly_rate']
            instructor_profile.save()
            # request.user.user_type = 'instructor'       
            request.user.is_instructor_pending = True
            request.user.save()
            messages.success(request, 'تم إرسال الطلب. في انتظار التحقق من الملائمة')
            return redirect('home')
        else:
            messages.error(request, 'خطأ أثناء تقديم الطلب.')
    else:
        form = BecomeInstructorForm()
    return render(request, 'users/become_instructor.html', {'form': form})