from django.contrib import admin
from django.utils.html import format_html
from .models import CourseSuggestion


@admin.register(CourseSuggestion)
class CourseSuggestionAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'user', 'suggestion_type', 'status', 'target_audience', 
        'estimated_duration', 'max_participants', 'created_at'
    )
    list_filter = ('suggestion_type', 'status', 'created_at')
    search_fields = ('title', 'description', 'user__username', 'target_audience', 'admin_notes')
    date_hierarchy = 'created_at'
    list_editable = ('status',)
    readonly_fields = ('created_at',)
    actions = ['approve_suggestions', 'reject_suggestions', 'mark_reviewing']

    fieldsets = (
        (None, {
            'fields': ('user', 'title', 'description', 'suggestion_type')
        }),
        ('التفاصيل', {
            'fields': ('target_audience', 'estimated_duration', 'max_participants', 'budget_range')
        }),
        ('الإدارة', {
            'fields': ('status', 'admin_notes', 'created_at')
        }),
    )

    def approve_suggestions(self, request, queryset):
        queryset.update(status='approved')
        self.message_user(request, "تمت الموافقة على الاقتراحات المختارة")
    approve_suggestions.short_description = "الموافقة على الاقتراحات المختارة"

    def reject_suggestions(self, request, queryset):
        queryset.update(status='rejected')
        self.message_user(request, "تم رفض الاقتراحات المختارة")
    reject_suggestions.short_description = "رفض الاقتراحات المختارة"

    def mark_reviewing(self, request, queryset):
        queryset.update(status='reviewing')
        self.message_user(request, "تم وضع علامة على اقتراحات مختارة على أنها قيد المراجعة")
    mark_reviewing.short_description = "وضع علامة قيد المراجعة"
