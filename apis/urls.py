from django.urls import path
from .views import QAView, QAListView

urlpatterns = [
    path('ask/', QAView.as_view(), name='ask-question'),
    path('history/', QAListView.as_view(), name='qa-history'),
]
