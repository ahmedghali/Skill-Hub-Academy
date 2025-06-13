from django.contrib import admin
from django.utils.html import format_html
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('course', 'student', 'rating_stars', 'is_active', 'comment_preview', 'created_at')
    list_filter = ('rating', 'is_active', 'created_at', 'course')
    search_fields = ('course__title', 'student__username', 'comment')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

    fieldsets = (
        (None, {
            'fields': ('course', 'student', 'is_active', 'rating', 'comment')
        }),
        ('البيانات الوصفية', {
            'fields': ('created_at',)
        }),
    )

    def rating_stars(self, obj):
        """Affiche la note sous forme d'étoiles."""
        return format_html('★' * obj.rating + '☆' * (5 - obj.rating))
    rating_stars.short_description = 'Note'

    def comment_preview(self, obj):
        """Affiche un aperçu du commentaire (50 premiers caractères)."""
        return obj.comment[:50] + ('...' if len(obj.comment) > 50 else '')
    comment_preview.short_description = 'Commentaire'