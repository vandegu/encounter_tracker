from django.urls import path, reverse_lazy
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.CreatureListView.as_view(), name='codex'),
    path('creature/<int:pk>', views.CreatureDetailView.as_view(), name='creature_detail'),
]
