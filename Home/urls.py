from django.urls import path
from .views import HomeView, QuoteCreateView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('submit-quote/', QuoteCreateView.as_view(), name='submit_quote'),
]