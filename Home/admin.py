# admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import EventType, Quote, QuoteComment


@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    """
    Admin for managing dynamic event types
    """
    list_display = ['name', 'display_order', 'is_active', 'icon_badge', 'quote_count']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    list_editable = ['display_order', 'is_active']
    ordering = ['display_order', 'name']
    fieldsets = (
        ('Event Type Information', {
            'fields': ('name', 'description', 'icon', 'is_active', 'display_order')
        }),
    )
    
    def icon_badge(self, obj):
        if obj.icon:
            return format_html('<i class="{}"></i>', obj.icon)
        return '-'
    icon_badge.short_description = 'Icon'
    
    def quote_count(self, obj):
        return obj.quotes.count()
    quote_count.short_description = 'Quotes'


class QuoteCommentInline(admin.TabularInline):
    model = QuoteComment
    extra = 1
    fields = ['comment', 'created_by', 'created_at']
    readonly_fields = ['created_at']


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    """
    Admin for managing quote requests
    """
    list_display = [
        'full_name', 
        'email', 
        'event_type_display', 
        'event_date_display',
        'budget_range_display',
        'status_badge', 
        'days_since_submitted'
    ]
    
    list_filter = [
        'status', 
        'event_type', 
        'budget_range',
        'how_did_you_hear',
        'created_at'
    ]
    
    search_fields = [
        'full_name', 
        'email', 
        'phone', 
        'message',
        'event_venue'
    ]
    
    readonly_fields = [
        'created_at', 
        'updated_at',
        'id'
    ]
    
    fieldsets = (
        ('Quote Information', {
            'fields': ('id', 'status', 'assigned_to')
        }),
        ('Contact Details', {
            'fields': ('full_name', 'email', 'phone')
        }),
        ('Event Details', {
            'fields': ('event_type', 'event_date', 'event_venue', 'estimated_guests')
        }),
        ('Budget & Services', {
            'fields': ('budget_range', 'services_required')
        }),
        ('Additional Information', {
            'fields': ('how_did_you_hear', 'message', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [QuoteCommentInline]
    
    actions = [
        'mark_as_pending',
        'mark_as_contacted', 
        'mark_as_in_progress',
        'mark_as_completed',
        'mark_as_archived'
    ]
    
    ordering = ['-created_at']
    list_per_page = 25
    date_hierarchy = 'created_at'
    
    def event_type_display(self, obj):
        return obj.event_type.name if obj.event_type else '-'
    event_type_display.short_description = 'Event Type'
    event_type_display.admin_order_field = 'event_type'
    
    def event_date_display(self, obj):
        if obj.event_date:
            return obj.event_date.strftime('%b %d, %Y')
        return 'Not specified'
    event_date_display.short_description = 'Event Date'
    
    def budget_range_display(self, obj):
        budget_labels = {
            'under_500': 'Under $500',
            '500_2000': '$500 - $2,000',
            '2000_5000': '$2,000 - $5,000',
            '5000_10000': '$5,000 - $10,000',
            'over_10000': 'Over $10,000',
            'not_specified': 'Not specified',
        }
        return budget_labels.get(obj.budget_range, obj.budget_range)
    budget_range_display.short_description = 'Budget'
    
    def status_badge(self, obj):
        status_styles = {
            'pending': {'color': '#f39c12', 'icon': '⏳', 'label': 'Pending'},
            'contacted': {'color': '#3498db', 'icon': '📞', 'label': 'Contacted'},
            'in_progress': {'color': '#9b59b6', 'icon': '🔄', 'label': 'In Progress'},
            'completed': {'color': '#27ae60', 'icon': '✅', 'label': 'Completed'},
            'archived': {'color': '#95a5a6', 'icon': '📦', 'label': 'Archived'},
        }
        style = status_styles.get(obj.status, {'color': '#95a5a6', 'icon': '❓', 'label': obj.status})
        
        return format_html(
            '<span style="color: {}; font-weight: bold;">{} {}</span>',
            style['color'],
            style['icon'],
            style['label']
        )
    status_badge.short_description = 'Status'
    status_badge.admin_order_field = 'status'
    
    def days_since_submitted(self, obj):
        if obj.created_at:
            days = (timezone.now() - obj.created_at).days
            if days == 0:
                return "Today"
            elif days == 1:
                return "Yesterday"
            else:
                return f"{days} days ago"
        return "-"
    days_since_submitted.short_description = 'Submitted'
    
    # Bulk actions
    def mark_as_pending(self, request, queryset):
        updated = queryset.update(status='pending')
        self.message_user(request, f'{updated} quote(s) marked as pending.')
    mark_as_pending.short_description = "Mark as Pending"
    
    def mark_as_contacted(self, request, queryset):
        updated = queryset.update(status='contacted')
        self.message_user(request, f'{updated} quote(s) marked as contacted.')
    mark_as_contacted.short_description = "Mark as Contacted"
    
    def mark_as_in_progress(self, request, queryset):
        updated = queryset.update(status='in_progress')
        self.message_user(request, f'{updated} quote(s) marked as in progress.')
    mark_as_in_progress.short_description = "Mark as In Progress"
    
    def mark_as_completed(self, request, queryset):
        updated = queryset.update(status='completed')
        self.message_user(request, f'{updated} quote(s) marked as completed.')
    mark_as_completed.short_description = "Mark as Completed"
    
    def mark_as_archived(self, request, queryset):
        updated = queryset.update(status='archived')
        self.message_user(request, f'{updated} quote(s) archived.')
    mark_as_archived.short_description = "Archive"
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('event_type')


@admin.register(QuoteComment)
class QuoteCommentAdmin(admin.ModelAdmin):
    list_display = ['quote', 'comment_preview', 'created_by', 'created_at']
    list_filter = ['created_at']
    search_fields = ['comment', 'created_by']
    readonly_fields = ['created_at']
    
    def comment_preview(self, obj):
        return obj.comment[:100] + '...' if len(obj.comment) > 100 else obj.comment
    comment_preview.short_description = 'Comment'


# Customize admin site
admin.site.site_header = "BluePrint AV Administration"
admin.site.site_title = "BluePrint AV Admin Portal"
admin.site.index_title = "Welcome to BluePrint AV Admin Dashboard"