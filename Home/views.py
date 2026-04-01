# views.py
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Quote
from .forms import QuoteModelForm

class HomeView(TemplateView):
    template_name = 'Home/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = QuoteModelForm()  # Pass empty form to template
        return context
    
class QuoteCreateView(CreateView):
    model = Quote
    form_class = QuoteModelForm
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        messages.success(
            self.request, 
            "Thank you! We'll get back to you within 24 hours."
        )
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(
            self.request, 
            "Please correct the errors below and try again."
        )
        return super().form_invalid(form)