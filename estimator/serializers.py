from rest_framework import serializers
from .models import Estimator,Output,Impact,SevereImpact



class OutputSerializer(serializers.ModelSerializer):
    class Meta:
        model= Output
        fields="__all__"
      

class EstimatorSerializer (serializers.ModelSerializer):
   
    class Meta:
        model= Estimator
        fields="__all__"
    
class ImpactSerializer(serializers.ModelSerializer):
    
    class Meta:
        model= Impact 
        fields="__all__"
      

class SevereImpactSerializer(serializers.ModelSerializer):
    class Meta:
        model= SevereImpact
        fields="__all__"
       

