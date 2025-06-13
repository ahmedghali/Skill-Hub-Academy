from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User, InstructorProfile


class InstructorProfileInline(admin.StackedInline):
    model = InstructorProfile
    can_delete = True
    extra = 0
    fields = ('specializations', 'experience_level', 'certification', 'hourly_rate', 'is_verified')
    readonly_fields = ('is_verified',)  # Peut être modifié via actions


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        'username', 'email', 'get_full_name', 'user_type', 
        'phone', 'profile_image_preview', 'date_of_birth', 
        'created_at', 'is_active', 'is_staff'
    )
    list_filter = ('user_type', 'is_active', 'is_staff', 'created_at')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone', 'bio')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')
    inlines = [InstructorProfileInline]
    actions = ['make_active', 'make_inactive']

    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('المعلومات الشخصية', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'bio', 'profile_image', 'date_of_birth')
        }),
        ('نوع المستخدم', {
            'fields': ('user_type',)
        }),
        ('التصاريح', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('التواريخ', {
            'fields': ('created_at', 'updated_at', 'last_login')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'user_type', 'phone', 'bio', 'profile_image', 'date_of_birth'),
        }),
    )

    def profile_image_preview(self, obj):
        if obj.profile_image:
            return format_html('<img src="{}" style="width: 50px; height: auto;" />', obj.profile_image)
        return "-"
    profile_image_preview.short_description = "صورة الملف الشخصي"

    def make_active(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, "تم تنشيط المستخدمين المحددينs")
    make_active.short_description = "تنشيط المستخدمين المحددينs"

    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, "تم إلغاء تنشيط المستخدمين المحددين")
    make_inactive.short_description = "إلغاء تنشيط المستخدمين المحددين"


@admin.register(InstructorProfile)
class InstructorProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'experience_level', 'is_verified', 
        'hourly_rate', 'specializations_preview'
    )
    list_filter = ('experience_level', 'is_verified')
    search_fields = ('user__username', 'user__email', 'specializations', 'certification')
    actions = ['verify_instructors', 'unverify_instructors']

    fieldsets = (
        (None, {
            'fields': ('user', 'specializations', 'experience_level')
        }),
        ('التفاصيل', {
            'fields': ('certification', 'hourly_rate', 'is_verified')
        }),
    )

    def specializations_preview(self, obj):
        return obj.specializations[:50] + ('...' if len(obj.specializations) > 50 else '')
    specializations_preview.short_description = 'التخصّصات'

    def verify_instructors(self, request, queryset):
        queryset.update(is_verified=True)
        self.message_user(request, "تم التحقق من ملفات تعريف المدربين المختارين")
    verify_instructors.short_description = "تحقق من ملفات تعريف المدربين"

    def unverify_instructors(self, request, queryset):
        queryset.update(is_verified=False)
        self.message_user(request, "لم يتم التحقق من ملفات تعريف المدربين الذين تم اختيارهم")
    unverify_instructors.short_description = "إزالة التحقق من ملفات تعريف المدربين"