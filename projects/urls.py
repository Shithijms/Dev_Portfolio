from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('project/<int:pk>/', views.project_detail, name='project_detail'),
    path('resume/', views.resume_view, name='resume'),
path('api/status/', views.api_status, name='api_status'),
]