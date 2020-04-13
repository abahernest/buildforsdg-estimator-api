from rest_framework import generics
from .models import Estimator
from .serializers import EstimatorSerializer


class ListTodo(generics.ListAPIView):
    queryset = Estimator.objects.all()
    serializer_class = EstimatorSerializer
class DetailTodo(generics.RetrieveAPIView):
    queryset = Estimator.objects.all()
    serializer_class = EstimatorSerializer