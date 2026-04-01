# forms.py
from django import forms
from .models import Quote

class QuoteModelForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ['full_name', 'email', 'phone', 'event_type', 'message']
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Your full name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email address'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone number (optional)'}),
            'event_type': forms.Select(),
            'message': forms.Textarea(attrs={'placeholder': 'Tell us about your event...'}),
        }