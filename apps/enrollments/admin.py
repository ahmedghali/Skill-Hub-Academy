from django.contrib import admin
from django.utils import timezone
from .models import Enrollment


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = (
        'student', 'course', 'session', 'status', 'enrolled_at', 
        'completed_at', 'is_active'
    )
    list_filter = ('status', 'is_active', 'enrolled_at', 'course', 'session')
    search_fields = ('student__username', 'course__title', 'session__location')
    date_hierarchy = 'enrolled_at'
    readonly_fields = ('enrolled_at',)
    list_editable = ('status', 'is_active')
    actions = ['confirm_enrollments', 'cancel_enrollments', 'mark_completed']

    fieldsets = (
        (None, {
            'fields': ('student', 'course', 'session', 'status')
        }),
        ('التواريخ', {
            'fields': ('enrolled_at', 'completed_at')
        }),
        ('الحالة', {
            'fields': ('is_active',)
        }),
    )

    def confirm_enrollments(self, request, queryset):
        queryset.update(status='confirmed', is_active=True)
        self.message_user(request, "تم تأكيد التسجيلات المختارة")
    confirm_enrollments.short_description = "تأكيد التسجيلات المختارة"

    def cancel_enrollments(self, request, queryset):
        queryset.update(status='cancelled', is_active=False)
        self.message_user(request, "تم إلغاء التسجيلات المحددة")
    cancel_enrollments.short_description = "إلغاء التسجيلات المحددة"

    def mark_completed(self, request, queryset):
        queryset.update(status='completed', completed_at=timezone.now(), is_active=False)
        self.message_user(request, "تم وضع علامة على التسجيلات المحددة على أنها مكتملة")
    mark_completed.short_description = "وضع علامة على التسجيلات على أنها مكتملة"