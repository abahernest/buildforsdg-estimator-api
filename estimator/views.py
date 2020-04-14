from rest_framework import viewsets
from .models import Estimator
from .serializers import EstimatorSerializer


class EstimatorViewSet (viewsets.ModelViewSet):
    queryset = Estimator.objects.all()
    serializer_class = EstimatorSerializer