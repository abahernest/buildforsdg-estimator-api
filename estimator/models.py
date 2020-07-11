from django.db import models


class Estimator (models.Model):
        name= models.CharField(max_length=50)
        avgAge = models.FloatField()
        avgDailyIncomeInUSD = models.FloatField()
        avgDailyIncomePopulation = models.FloatField()
        periodType = models.CharField(max_length=10)
        timeToElapse= models.IntegerField()
        reportedCases = models.IntegerField()
        population = models.IntegerField()
        totalHospitalBeds=models.IntegerField()

class Impact (models.Model):
        currentlyInfected = models.IntegerField()
        infectionsByRequestedTime = models.IntegerField()
        severeCasesByRequestedTime= models.FloatField()
        hospitalBedsByRequestedTime = models.FloatField()
        casesForICUByRequestedTime = models.FloatField()
        casesForVentilatorsByRequestedTime = models.FloatField()
        dollarsInFlight = models.FloatField()


class SevereImpact (models.Model):
        currentlyInfected = models.IntegerField()
        infectionsByRequestedTime = models.IntegerField()
        severeCasesByRequestedTime= models.FloatField()
        hospitalBedsByRequestedTime = models.FloatField()
        casesForICUByRequestedTime = models.FloatField()
        casesForVentilatorsByRequestedTime = models.FloatField()
        dollarsInFlight = models.FloatField()

class Output (models.Model):
        input_data=models.ForeignKey(Estimator,on_delete=models.PROTECT)
        impact = models.ForeignKey(Impact, on_delete=models.PROTECT)
        severeImpact= models.ForeignKey(SevereImpact, on_delete=models.PROTECT)
