from django.urls import path, reverse_lazy
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.CreatureListView.as_view())
]
