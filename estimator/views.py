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
from django.shortcuts import get_object_or_404


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

            output_serializer = OutputSerializer(data=output_data)
            if output_serializer.is_valid():
                output_serializer.save()

            impact_serializer=ImpactSerializer(data=output_data['impact'])
            if impact_serializer.is_valid():
                impact_serializer.save()

            severeImpact_serializer=SevereImpactSerializer(data=output_data['severeImpact'])
            if severeImpact_serializer.is_valid():
                severeImpact_serializer.save()
            

            # return Response ({'input_data':output_serializer.data['input_data'],"impact":output_serializer.data['impact'],'severeImpact':output_serializer.data['severeImpact']})
            return Response(output_serializer.data)
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
        estimator = get_object_or_404(Estimator,pk=pk)
        serializer = EstimatorSerializer(estimator)

        impact = get_object_or_404(Impact, pk=pk)
        impact_serializer = ImpactSerializer(impact)

        severeimpact = get_object_or_404(SevereImpact, pk=pk)
        severeImpact_serializer = SevereImpactSerializer (severeimpact)

        return Response({'input_data':serializer.data,'impact':impact_serializer.data,'severeImpact':severeImpact_serializer.data})



    def put(self, request, pk, format=None):
        estimator = get_object_or_404(Estimator,pk=pk)
        serializer = EstimatorSerializer(estimator, data=request.data)
        if serializer.is_valid():
            serializer.save()
        
            # output_data = estimator_function(serializer.data)
            # id= serializer.data['id']
            # Impact.objects.filter(pk=id).update(
            #     output_data['impact']["currentlyInfected"], 
            #     output_data['impact']["infectionsByRequestedTime"],
            #     output_data['impact']["severeCasesByRequestedTime"],
            #     output_data['impact']["hospitalBedsByRequestedTime"],
            #     output_data['impact']["casesForICUByRequestedTime"],
            #     output_data['impact']["casesForVentilatorsByRequestedTime"],
            #     output_data['impact']["dollarsInFlight"])
            
            # SevereImpact.objects.filter(pk=id).update(
            #     output_data['severeImpact']["currentlyInfected"],
            #     output_data['severeImpact']["infectionsByRequestedTime"],
            #     output_data['severeImpact']["severeCasesByRequestedTime"],
            #     output_data['severeImpact']["hospitalBedsByRequestedTime"],
            #     output_data['severeImpact']["casesForICUByRequestedTime"],
            #     output_data['severeImpact']["casesForVentilatorsByRequestedTime"],
            #     output_data['severeImpact']["dollarsInFlight"])
            
            # return Response({'input_data': serializer.data, 'impact':output_data.impact,'severeImpact': output_data.severeImpact})
            return Response (serializer.data)
        return JsonResponse({"message":"Invalid Input"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        estimator = get_object_or_404(Estimator,pk=pk)
        impact = get_object_or_404(Impact, pk=pk)
        severeImpact = get_object_or_404(SevereImpact, pk=pk)
        
        estimator.delete()
        impact.delete()
        severeImpact.delete()
        return JsonResponse({"message":"Successfully Deleted"},status=status.HTTP_204_NO_CONTENT)


    
