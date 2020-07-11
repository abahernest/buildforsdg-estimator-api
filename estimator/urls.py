from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('api/v1/on-covid-19/', views.EstimatorListView.as_view()),
    path('api/v1/on-covid-19/<int:pk>/', views.EstimatorDetailView.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)

