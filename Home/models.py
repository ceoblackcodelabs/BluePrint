# models.py
from django.db import models
from django.utils import timezone

class EventType(models.Model):
    """
    Model to store dynamic event types that can be managed from admin
    """
    name = models.CharField(max_length=100, unique=True, help_text="Event type name (e.g., Corporate Event)")
    description = models.TextField(blank=True, help_text="Optional description of this event type")
    icon = models.CharField(max_length=50, blank=True, help_text="Font Awesome icon class (e.g., fas fa-briefcase)")
    is_active = models.BooleanField(default=True, help_text="Show this event type in forms")
    display_order = models.IntegerField(default=0, help_text="Order to display in dropdown")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['display_order', 'name']
        verbose_name = 'Event Type'
        verbose_name_plural = 'Event Types'
    
    def __str__(self):
        return self.name


class Quote(models.Model):
    """
    Model to store quote requests from the website
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('contacted', 'Contacted'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('archived', 'Archived'),
    ]
    
    # Personal Information
    full_name = models.CharField(max_length=200, verbose_name="Full Name")
    email = models.EmailField(verbose_name="Email Address")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Phone Number")
    
    # Event Details
    event_type = models.ForeignKey(
        EventType, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='quotes',
        verbose_name="Event Type"
    )
    event_date = models.DateField(null=True, blank=True, verbose_name="Event Date")
    event_venue = models.CharField(max_length=255, blank=True, verbose_name="Event Venue")
    estimated_guests = models.PositiveIntegerField(null=True, blank=True, verbose_name="Estimated Guests")
    
    # Budget Information
    budget_range = models.CharField(
        max_length=50, 
        blank=True,
        choices=[
            ('under_500', 'Under $500'),
            ('500_2000', '$500 - $2,000'),
            ('2000_5000', '$2,000 - $5,000'),
            ('5000_10000', '$5,000 - $10,000'),
            ('over_10000', 'Over $10,000'),
            ('not_specified', 'Not specified'),
        ],
        default='not_specified',
        verbose_name="Budget Range"
    )
    
    # Service Requirements
    services_required = models.JSONField(
        default=list,
        blank=True,
        help_text="List of services required (Audio, Visual, Lighting, etc.)",
        verbose_name="Services Required"
    )
    
    # Additional Information
    message = models.TextField(verbose_name="Message / Requirements")
    how_did_you_hear = models.CharField(
        max_length=100, 
        blank=True,
        choices=[
            ('google', 'Google Search'),
            ('social_media', 'Social Media'),
            ('referral', 'Referral'),
            ('event', 'Saw at an event'),
            ('advertisement', 'Advertisement'),
            ('other', 'Other'),
        ],
        default='other',
        verbose_name="How did you hear about us?"
    )
    
    # Status and Tracking
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending',
        verbose_name="Quote Status"
    )
    assigned_to = models.CharField(max_length=100, blank=True, verbose_name="Assigned To")
    notes = models.TextField(blank=True, verbose_name="Internal Notes")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Submitted On")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Last Updated")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Quote Request'
        verbose_name_plural = 'Quote Requests'
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['event_type']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.full_name} - {self.event_type} - {self.created_at.strftime('%Y-%m-%d')}"
    
    def get_service_list(self):
        """Return services as a readable list"""
        if isinstance(self.services_required, list):
            return ', '.join(self.services_required)
        return ''
    
    def is_new(self):
        """Check if quote was submitted in the last 24 hours"""
        return (timezone.now() - self.created_at).days < 1
    
    def response_time(self):
        """Calculate response time if status is contacted"""
        # This would require tracking when status changed
        pass


class QuoteComment(models.Model):
    """
    Model to store internal comments on quotes (useful for team collaboration)
    """
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    created_by = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
        verbose_name = 'Quote Comment'
        verbose_name_plural = 'Quote Comments'
    
    def __str__(self):
        return f"Comment on {self.quote.full_name} - {self.created_at.strftime('%Y-%m-%d')}"

