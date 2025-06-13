from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course, CourseSession, Category
from .forms import CourseForm, CourseFormAdmin, CourseSessionForm
from django.utils.text import slugify



def course_list(request):
    # courses = Course.objects.filter(is_active=True)
    courses = Course.objects.filter(is_active=True).order_by('-created_at')
    context = {'courses': courses}
    return render(request, 'courses/course_list.html', context)

def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    sessions = course.sessions_course.filter(is_cancelled=False)
    projects = course.projects_course.all()
    context = {
        'course': course,
        'sessions': sessions,
        'projects': projects,
    }
    return render(request, 'courses/course_detail.html', context)

def category_list(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'courses/category_list.html', context)


@login_required
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.user != course.instructor:
        messages.error(request, 'لا يمكنك حذف هذه الدورة.')
        return redirect('home')
    if request.method == 'POST':
        course.delete()
        messages.success(request, 'تم حذف الدورة بنجاح!')
        return redirect('profile_pro')
    return render(request, 'courses/course_confirm_delete.html', {'course': course})

@login_required
def course_session_create(request, course_pk):
    course = get_object_or_404(Course, pk=course_pk)
    if request.user != course.instructor:
        messages.error(request, 'لا يمكنك إضافة جلسة لهذه الدورة.')
        return redirect('home')
    if request.method == 'POST':
        form = CourseSessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.course = course
            session.save()
            messages.success(request, 'تم إضافة الجلسة بنجاح!')
            return redirect('courses:course_detail', pk=course.pk)
        else:
            messages.error(request, 'خطأ أثناء إضافة الجلسة.')
    else:
        form = CourseSessionForm()
    return render(request, 'courses/session_form.html', {'form': form, 'course': course})

@login_required
def course_session_update(request, course_pk, session_pk):
    course = get_object_or_404(Course, pk=course_pk)
    session = get_object_or_404(CourseSession, pk=session_pk, course=course)
    if request.user != course.instructor:
        messages.error(request, 'لا يمكنك تعديل هذه الجلسة.')
        return redirect('home')
    if request.method == 'POST':
        form = CourseSessionForm(request.POST, instance=session)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تعديل الجلسة بنجاح!')
            return redirect('courses:course_detail', pk=course.pk)
        else:
            messages.error(request, 'خطأ أثناء تعديل الجلسة.')
    else:
        form = CourseSessionForm(instance=session)
    return render(request, 'courses/session_form.html', {'form': form, 'course': course, 'action': 'تعديل'})

@login_required
def course_session_delete(request, course_pk, session_pk):
    course = get_object_or_404(Course, pk=course_pk)
    session = get_object_or_404(CourseSession, pk=session_pk, course=course)
    if request.user != course.instructor:
        messages.error(request, 'لا يمكنك حذف هذه الجلسة.')
        return redirect('home')
    if request.method == 'POST':
        session.delete()
        messages.success(request, 'تم حذف الجلسة بنجاح!')
        return redirect('courses:course_detail', pk=course.pk)
    return render(request, 'courses/session_confirm_delete.html', {'session': session, 'course': course})



from django.core.paginator import Paginator
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    courses = Course.objects.filter(category=category, is_active=True)
    paginator = Paginator(courses, 9)  # 9 cours par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'category': category, 'page_obj': page_obj}
    return render(request, 'courses/course_category_detail.html', context)




from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Category, Course
from .forms import CategoryForm

def category_list(request):
    categories = Category.objects.all().order_by('name')
    return render(request, 'courses/category_list.html', {'categories': categories})

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    courses = category.courses_category.all().order_by('title')
    return render(request, 'courses/category_detail.html', {'category': category, 'courses': courses})





@login_required
def category_create(request):
    if request.user.user_type != 'admin':
        return HttpResponseForbidden("ليس لديك صلاحية لإنشاء فئة.")
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم إنشاء الفئة بنجاح!')
            return redirect('courses:category_list')
        else:
            messages.error(request, 'يرجى تصحيح الأخطاء أدناه.')
    else:
        form = CategoryForm()
    return render(request, 'courses/category_form.html', {'form': form, 'title': 'إنشاء فئة جديدة'})



@login_required
def category_update(request, slug):
    if request.user.user_type != 'admin':
        return HttpResponseForbidden("ليس لديك صلاحية لتعديل فئة.")
    category = get_object_or_404(Category, slug=slug)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تحديث الفئة بنجاح!')
            return redirect('courses:category_list')
        else:
            messages.error(request, 'يرجى تصحيح الأخطاء أدناه.')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'courses/category_form.html', {'form': form, 'title': 'تعديل الفئة', 'category': category})

@login_required
def category_delete(request, slug):
    if request.user.user_type != 'admin':
        return HttpResponseForbidden("ليس لديك صلاحية لحذف فئة.")
    category = get_object_or_404(Category, slug=slug)
    if request.method == 'POST':
        if category.can_delete:
            category.delete()
            messages.success(request, 'تم حذف الفئة بنجاح!')
        else:
            messages.error(request, 'لا يمكن حذف هذه الفئة لأنها مرتبطة بدورات.')
        return redirect('courses:category_list')
    return render(request, 'courses/category_confirm_delete.html', {'category': category})




from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Project, Course
from .forms import ProjectForm

@login_required
def project_list(request):
    if request.user.user_type != 'instructor':
        return HttpResponseForbidden("ليس لديك صلاحية لعرض المشاريع.")
    projects = Project.objects.filter(course__instructor=request.user).order_by('order')
    return render(request, 'courses/project_list.html', {'projects': projects})

@login_required
def project_create(request):
    if request.user.user_type != 'instructor':
        return HttpResponseForbidden("ليس لديك صلاحية لإنشاء مشروع.")
    if request.method == 'POST':
        form = ProjectForm(request.POST, user=request.user)
        if form.is_valid():
            project = form.save()
            messages.success(request, 'تم إنشاء المشروع بنجاح!')
            return redirect('courses:project_list')
        else:
            messages.error(request, 'يرجى تصحيح الأخطاء أدناه.')
    else:
        form = ProjectForm(user=request.user)
    return render(request, 'courses/project_form.html', {'form': form, 'title': 'إنشاء مشروع جديد'})


@login_required
def project_update(request, pk):
    if request.user.user_type != 'instructor':
        return HttpResponseForbidden("ليس لديك صلاحية لتعديل المشروع.")
    project = get_object_or_404(Project, pk=pk, course__instructor=request.user)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تعديل المشروع بنجاح!')
            return redirect('courses:project_list')
        else:
            messages.error(request, 'يرجى تصحيح الأخطاء أدناه.')
    else:
        form = ProjectForm(instance=project, user=request.user)
    return render(request, 'courses/project_form.html', {'form': form, 'title': 'تعديل المشروع'})

@login_required
def project_delete(request, pk):
    if request.user.user_type != 'instructor':
        return HttpResponseForbidden("ليس لديك صلاحية لحذف المشروع.")
    project = get_object_or_404(Project, pk=pk, course__instructor=request.user)
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'تم حذف المشروع بنجاح!')
        return redirect('courses:project_list')
    return render(request, 'courses/project_confirm_delete.html', {'project': project})




@login_required
def course_list_admin(request):
    if request.user.user_type != 'admin':
        return HttpResponseForbidden("ليس لديك صلاحية لعرض الدورات.")
    courses = Course.objects.all().order_by('-created_at')
    return render(request, 'courses/course_list_admin.html', {'courses': courses})




@login_required
def course_create(request):
    if request.user.user_type != 'instructor':
        return HttpResponseForbidden("ليس لديك صلاحية لإنشاء دورة.")
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user
            course.slug = slugify(course.title)
            course.save()
            messages.success(request, 'تم إنشاء الدورة بنجاح!')
            return redirect('profile_pro')
        else:
            messages.error(request, 'يرجى تصحيح الأخطاء أدناه.')
    else:
        form = CourseForm()
    return render(request, 'courses/course_form.html', {'form': form, 'title': 'إنشاء دورة جديدة'})

@login_required
def course_update(request, pk):
    if request.user.user_type != 'instructor':
        return HttpResponseForbidden("ليس لديك صلاحية لتعديل الدورة.")
    course = get_object_or_404(Course, pk=pk, instructor=request.user)  # Vérifie que le cours appartient à l'instructor
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)  # Ajout de request.FILES
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user  # Redondant mais conservé pour cohérence
            course.slug = slugify(course.title)
            course.save()
            messages.success(request, 'تم تعديل الدورة بنجاح!')
            return redirect('profile_pro')
        else:
            messages.error(request, 'يرجى تصحيح الأخطاء أدناه.')
    else:
        form = CourseForm(instance=course)
    return render(request, 'courses/course_form.html', {'form': form, 'title': 'تعديل الدورة', 'action': 'تعديل'})



@login_required
def course_update_admin(request, slug):
    if request.user.user_type != 'admin':
        return HttpResponseForbidden("ليس لديك صلاحية لتعديل الدورة.")
    course = get_object_or_404(Course, slug=slug)
    if request.method == 'POST':
        form = CourseFormAdmin(request.POST, instance=course)
        if form.is_valid():
            course = form.save(commit=False)
            course.slug = slugify(course.title)
            course.save()
            messages.success(request, 'تم تعديل الدورة بنجاح!')
            return redirect('courses:course_list_admin')
        else:
            messages.error(request, 'يرجى تصحيح الأخطاء أدناه.')
    else:
        form = CourseFormAdmin(instance=course)
    return render(request, 'courses/course_update_admin.html', {'form': form, 'title': 'تعديل الدورة'})




# @login_required
# def instructor_application(request):
#     if request.user.user_type == 'instructor':
#         messages.warning(request, 'أنت بالفعل مدرس.')
#         return redirect('home')
#     if request.method == 'POST':
#         form = InstructorApplicationForm(request.POST, request.FILES)
#         if form.is_valid():
#             application = form.save(commit=False)
#             application.user = request.user
#             application.save()
#             messages.success(request, 'تم إرسال طلبك ليصبح مدرسًا!')
#             return redirect('home')
#     else:
#         form = InstructorApplicationForm()
#     return render(request, 'courses/instructor_application.html', {'form': form})