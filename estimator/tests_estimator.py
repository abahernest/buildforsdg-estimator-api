from django.test import TestCase
# import unittest
from .estimator import estimator_function,duration_normaliser,available_beds,money_lost

class DurationNormalizerTestCase (TestCase):
    def test_duration_is_days (self):
        duration,value="days",200
        expected=200
        self.assertEqual (duration_normaliser(duration,value),expected)

    def test_duration_is_day (self):
        duration,value ="days",0
        expected=0
        self.assertEqual (duration_normaliser(duration,value),expected)

    def test_should_return_value_times_30_when_duration_value_is_months(self):
        duration,value ="months",7
        expected= value*30
        self.assertEqual (duration_normaliser(duration,value),expected)

    def test_should_return_value_times_30_when_duration_value_is_month (self):
        duration,value ="month",300
        expected= value*30
        self.assertEqual (duration_normaliser(duration,value),expected)

    def test_should_return_same_value_when_duration_type_is_unrecognized (self):
        duration,value ="blaahs",30
        expected=30
        self.assertEqual (duration_normaliser(duration,value),expected)

    def test_should_return_value_of_corresponding_duration_type_if_duration_value_is_negative (self):
        duration, value = "months", -5
        expected=30
        self.assertEqual (duration_normaliser(duration,value),expected)   

    def test_should_return_0_if_duration_type_is_unrecognized_and_duration_value_is_negative (self):
        duration, value = "blaahs", -30
        expected = 0
        self.assertEqual(duration_normaliser(duration, value), expected)


class AvailableBedsTestCase (TestCase):
    def test_total_beds_is_less_than_severe_cases (self):
        total_beds,severe_cases = 2,10
        expected=int(0.35*total_beds - severe_cases)
        self.assertEqual (available_beds(total_beds,severe_cases),expected)
    
    def test_total_beds_is_more_than_severe_cases (self):
        total_beds, severe_cases = 10, 2
        expected=int(0.35*total_beds - severe_cases)
        self.assertEqual(available_beds(total_beds,severe_cases),expected)

    def test_should_be_negative_if_total_beds_is_equal_to_severe_cases(self):
        total_beds, severe_cases = 10, 10
        expected = int(0.35*total_beds - severe_cases)
        self.assertTrue(available_beds(total_beds, severe_cases)<0)

    def test_should_be_zero_if_total_beds_is_negative(self):
        total_beds, severe_cases = -1, 10
        expected = 0
        self.assertEqual(available_beds(total_beds, severe_cases),expected)

    def test_should_be_zero_if_severe_cases_is_negative(self):
        total_beds, severe_cases = 10, -3
        expected = 0
        self.assertEqual(available_beds(total_beds, severe_cases), expected)


class MoneyLostTestCase (TestCase):
    def simple_test (self):
        days,avgIncome,avgIncomePopulation = 30,7.5,0.71
        expected = (avgIncome*avgIncomePopulation)/days
        self.assertEqual(money_lost(days,avgIncome,avgIncomePopulation),expected)

    def tests_should_return_zero_if_days_is_zero (self):
        days,avgIncome,avgIncomePopulation = 0,7.5,0.71
        expected = 0
        self.assertEqual(money_lost(days,avgIncome,avgIncomePopulation),expected)   

    def tests_should_return_zero_if_days_is_negative (self):
        days, avgIncome, avgIncomePopulation = -12, 7.5, 0.71
        expected = 0
        self.assertEqual(money_lost(days, avgIncome, avgIncomePopulation), expected)
