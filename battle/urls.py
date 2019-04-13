from django.urls import path, reverse_lazy
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('create',views.BattleCreateView.as_view(success_url=reverse_lazy('home')), name='battle_create'),
    path('encounter/<int:pk>', views.BattleDetailView.as_view(), name='battle_detail'),
    path('encounter/<int:pk>/delete',
        views.BattleDeleteView.as_view(), name='battle_delete'),
]
