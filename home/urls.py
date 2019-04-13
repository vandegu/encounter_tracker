from django.urls import path, reverse_lazy
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.HomeView.as_view(),name='home'),
    path('createuser', views.CreateUser.as_view(),name='create_user')
]
