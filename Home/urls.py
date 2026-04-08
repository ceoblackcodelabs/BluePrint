from django.urls import path
from .views import HomeView, QuoteCreateView, ServiceDetailView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('submit-quote/', QuoteCreateView.as_view(), name='submit_quote'),
    path('service/<slug:slug>/', ServiceDetailView.as_view(), name='service_detail'),
]