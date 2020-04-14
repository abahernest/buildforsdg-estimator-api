from django.utils.decorators import method_decorator #for caching
from django.views.decorators.cache import cache_page #for caching
from rest_framework.response import Response
from django.http import JsonResponse,HttpResponse
from rest_framework.views import APIView
from .serializers import EstimatorSerializer,OutputSerializer,ImpactSerializer,SevereImpactSerializer
from .models import Estimator,Impact,Output,SevereImpact
from .estimator import estimator_function
from rest_framework import status,generics
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser


import time



class EstimatorListView (APIView):
    """
                INPUT FORMAT:
            
                    "name": ,

                    "avgAge": ,

                    "avgDailyIncomeInUSD": ,

                    "avgDailyIncomePopulation": ,

                    "periodType": ,

                    "timeToElapse": ,
                    
                    "reportedCases": ,

                    "population": ,

                    "totalHospitalBeds": 
                
    """
    #@method_decorator(cache_page(60*60*2))
    #serializer_class=serializers.EstimatorSerializer
    ###GET
    def get (self, request, format=None):   
        estimator=Estimator.objects.all()
        impact=Impact.objects.all()
        severeimpact=SevereImpact.objects.all()
       
        serializer=EstimatorSerializer(estimator,many=True)
        impact_serializer=ImpactSerializer(impact,many=True)
        severeImpact_serializer=SevereImpactSerializer(severeimpact, many=True)

        return Response ({'input':serializer.data,'impact':impact_serializer.data,'severeImpact':severeImpact_serializer.data})
    

    
    ###POST
    def post(self,request,format=None):
        data = JSONParser().parse(request)
        serializer = EstimatorSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            output_data=estimator_function(serializer.data)

            impact_serializer=ImpactSerializer(data=output_data['impact'])
            if impact_serializer.is_valid():
                impact_serializer.save()

            severeImpact_serializer=SevereImpactSerializer(data=output_data['severeImpact'])
            if severeImpact_serializer.is_valid():
                severeImpact_serializer.save()
            
            output_serializer = OutputSerializer(data=output_data)
            if output_serializer.is_valid():
                output_serializer.save()
            return Response ({'input_data':output_serializer.data['input_data'],"impact":output_serializer.data['impact'],'severeImpact':output_serializer.data['severeImpact']})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class EstimatorDetailView(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return Estimator.objects.get(pk=pk)
        except Estimator.DoesNotExist:
            Response(status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk, format=None):
        estimator = self.get_object(pk)
        serializer = EstimatorSerializer(estimator)
        impact_serializer = ImpactSerializer(Impact.objects.get(pk=pk))
        severeImpact_serializer = SevereImpactSerializer (SevereImpact.objects.get(pk=pk))
        return Response({'input_data':serializer.data,'impact':impact_serializer.data,'severeImpact':severeImpact_serializer.data})

    def put(self, request, pk, format=None):
        estimator = self.get_object(pk)
        serializer = EstimatorSerializer(estimator, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        estimator = self.get_object(pk)
        estimator.delete()
        impact = Impact.objects.get(pk=pk)
        impact.delete()
        severeImpact=SevereImpact.objects.get(pk=pk)
        severeImpact.delete()
        #return Response(status=status.HTTP_204_NO_CONTENT)


    
