from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Course, CourseSession, Project


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']
    prepopulated_fields = {'description': ('name',)}
    date_hierarchy = 'created_at'

    def icon_preview(self, obj):
        if obj.icon:
            return format_html('<img src="{}" style="width: 50px; height: auto;" />', obj.icon)
        return "-"
    icon_preview.short_description = "Icône"

    def course_count(self, obj):
        return obj.courses_category.count()
    course_count.short_description = "عدد الدورات"


class CourseSessionInline(admin.TabularInline):
    model = CourseSession
    extra = 1
    fields = ('start_date', 'end_date', 'location', 'meeting_link', 'current_participants', 'is_cancelled')
    readonly_fields = ('current_participants',)
    show_change_link = True


class ProjectInline(admin.StackedInline):
    model = Project
    extra = 1
    fields = ('title', 'description', 'resources', 'order')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'category', 'instructor', 'delivery_mode', 'target_audience', 
        'difficulty_level', 'price', 'enrolled_count', 'average_rating', 
        'is_active', 'is_featured', 'created_at'
    )
    list_filter = (
        'category', 'delivery_mode', 'target_audience', 'difficulty_level', 
        'is_active', 'is_featured', 'created_at'
    )
    search_fields = ('title', 'description', 'objectives', 'instructor__username')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    inlines = [CourseSessionInline, ProjectInline]
    actions = ['make_active', 'make_inactive', 'make_featured', 'remove_featured']
    readonly_fields = ('created_at', 'updated_at', 'enrolled_count', 'average_rating')
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'description', 'objectives', 'category', 'instructor')
        }),
        ('تفاصيل الدورة', {
            'fields': (
                'price', 'duration_hours', 'max_participants', 'min_participants', 
                'delivery_mode', 'target_audience', 'difficulty_level'
            )
        }),
        ('المتطلبات والمعدات', {
            'fields': ('prerequisites', 'required_materials')
        }),
        ('الوسائط', {
            'fields': ('thumbnail', 'intro_video')
        }),
        ('البيانات الوصفية', {
            'fields': ('is_active', 'is_featured', 'created_at', 'updated_at', 'enrolled_count', 'average_rating')
        }),
    )

    def make_active(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, "تم تفعيل الدورات المختارة.")
    make_active.short_description = "تفعيل الدورات المحددة"

    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, "تم إلغاء تنشيط دورات مختارة")
    make_inactive.short_description = "إلغاء تنشيط دورات محددة"

    def make_featured(self, request, queryset):
        queryset.update(is_featured=True)
        self.message_user(request, "تم تسليط الضوء على دورات مختارة")
    make_featured.short_description = "تسليط الضوء على دورات مختارة"

    def remove_featured(self, request, queryset):
        queryset.update(is_featured=False)
        self.message_user(request, "لم يعد يتم تمييز الدورات المختارة")
    remove_featured.short_description = "إزالة إبراز الدورات المحددة"


@admin.register(CourseSession)
class CourseSessionAdmin(admin.ModelAdmin):
    list_display = ('course', 'start_date', 'end_date', 'location', 'meeting_link', 'current_participants', 'is_cancelled')
    list_filter = ('course', 'start_date', 'is_cancelled')
    search_fields = ('course__title', 'location', 'meeting_link')
    date_hierarchy = 'start_date'
    readonly_fields = ('current_participants',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)
    search_fields = ('title', 'description', 'course__title')
    ordering = ('course', 'order')