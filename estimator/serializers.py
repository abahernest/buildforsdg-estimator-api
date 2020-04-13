from rest_framework import serializers
from .models import Estimator


class EstimatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estimator
        fields = "__all__"