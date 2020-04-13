from django.db import models


class Estimator (models.Model):
        name= models.CharField(max_length=50)
        avgDailyIncomeInUSD = models.FloatField()
        avgAge = models.FloatField()
        avgDailyIncomePopulation = models.FloatField()
        periodType = models.CharField(max_length=10)
        timeToElapse= models.IntegerField()
        reportedCases = models.IntegerField()
        population = models.IntegerField()
        totalHospitalBeds=models.IntegerField()
