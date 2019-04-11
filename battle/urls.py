from django.urls import path, reverse_lazy
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('create',views.BattleCreateView.as_view(), name='battle_create'),
]
