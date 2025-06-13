from django.contrib import admin
from django.utils.html import format_html
from .models import GeneralFeedback


@admin.register(GeneralFeedback)
class GeneralFeedbackAdmin(admin.ModelAdmin):
    list_display = (
        'subject', 'user', 'feedback_type', 'message_preview', 
        'is_resolved', 'created_at'
    )
    list_filter = ('feedback_type', 'is_resolved', 'created_at')
    search_fields = ('subject', 'message', 'user__username', 'admin_response')
    date_hierarchy = 'created_at'
    list_editable = ('is_resolved',)
    readonly_fields = ('created_at',)
    actions = ['mark_resolved', 'mark_unresolved']

    fieldsets = (
        (None, {
            'fields': ('user', 'feedback_type', 'subject', 'message')
        }),
        ('الإدارة', {
            'fields': ('is_resolved', 'admin_response', 'created_at')
        }),
    )

    def message_preview(self, obj):
        """Affiche un aperçu du message (50 premiers caractères)."""
        return obj.message[:50] + ('...' if len(obj.message) > 50 else '')
    message_preview.short_description = 'Message'

    def mark_resolved(self, request, queryset):
        queryset.update(is_resolved=True)
        self.message_user(request, "تم وضع علامة على المراجعات المحددة على أنها تم حلها")
    mark_resolved.short_description = "وضع علامة تم حلها"

    def mark_unresolved(self, request, queryset):
        queryset.update(is_resolved=False)
        self.message_user(request, "تم وضع علامة على المراجعات المحددة على أنها لم يتم حلها")
    mark_unresolved.short_description = "وضع علامة لم يتم حلها"