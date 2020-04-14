from django.urls import path,include
from .views import EstimatorViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register (r'estimator',EstimatorViewSet)

urlpatterns = [
path('api/v1/on-covid-19/', include(router.urls)),
]