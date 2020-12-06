from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from estimator.models import *


class EstimatorListViewTestCase (APITestCase):
    def setUp (self):
        self.data = {"name": "Africa",
                "avgAge": 19.7,
                "avgDailyIncomeInUSD": 5,
                "avgDailyIncomePopulation": 0.71,
                "periodType": "days",
                "timeToElapse": 58,
                "reportedCases": 674,
                "population": 66622705,
                "totalHospitalBeds": 1380614
                }
            
    def test_should_return_200_status_code_on_post_method (self):
        url = "/api/v1/on-covid-19/"
        res=self.client.post(url,self.data,format="json")
        self.assertEqual (res.status_code,200)
        with self.subTest():
            self.assertEqual(Estimator.objects.count(), 1)
            

    def test_should_return_a_dictionary_that_contains_input_data_on_post_request (self):
        url = "/api/v1/on-covid-19/"
        res = self.client.post(url,self.data,format="json")
        self.assertNotEqual (res.data['input_data'],[])
        with self.subTest(res=res):
            self.assertNotEqual(res.data['impact'], [])
            self.assertNotEqual (res.data['severeImpact'],[])

    def test_that_objects_created_during_post_request_are_saved_in_db (self):
            url = "/api/v1/on-covid-19/"
            NUMBER_OF_OBJECTS = 4
            for count in range(NUMBER_OF_OBJECTS):
                self.client.post(url, self.data, format="json")

            self.assertEqual(Estimator.objects.count(), NUMBER_OF_OBJECTS)
            self.assertEqual(Impact.objects.count(), NUMBER_OF_OBJECTS)
            self.assertEqual(SevereImpact.objects.count(), NUMBER_OF_OBJECTS)

    def test_should_return_400_status_on_invalid_input_to_post_method (self):
        url = "/api/v1/on-covid-19/"
        data = {
                "avgAge": 19.7,
                "avgDailyIncomeInUSD": 5,
                "avgDailyIncomePopulation": 0.71,
                
                "timeToElapse": 58,
                
                "population": 66622705,
                "totalHospitalBeds": 1380614
                }

        res = self.client.post(url, data, format="json")
        self.assertEqual (res.status_code,400)

    def test_should_return_all_estimator_objects_on_get_request (self):
        url = "/api/v1/on-covid-19/"
        NUMBER_OF_OBJECTS=4
        for count in range (NUMBER_OF_OBJECTS):
            self.client.post(url,self.data,format="json")

        res = self.client.get(url)
        self.assertEqual (res.status_code,200)
        self.assertEqual (len(res.data['input']),NUMBER_OF_OBJECTS)
        self.assertEqual (len(res.data['impact']), NUMBER_OF_OBJECTS)
        self.assertEqual(len(res.data['severeImpact']), NUMBER_OF_OBJECTS)


class EstimatorDetailViewTestCase (APITestCase):
    def setUp(self):
        url="/api/v1/on-covid-19/"
        for count in range(1,6):
            self.client.post(url, {"name": f"Africa{count}",
                                   "avgAge": 19.7,
                                   "avgDailyIncomeInUSD": 5,
                                   "avgDailyIncomePopulation": 0.71,
                                   "periodType": "days",
                                   "timeToElapse": 58,
                                   "reportedCases": 674,
                                   "population": 66622705,
                                   "totalHospitalBeds": 1380614
                                   }, format='json')

    def test_should_return_object_at_given_id (self):
        url = "/api/v1/on-covid-19/1/"
        res=self.client.get(url)
        self.assertEqual(res.data['input_data']['name'],"Africa1")
        with self.subTest(res=res):
            self.assertNotEqual (res.data['impact'],[])
            self.assertNotEqual (res.data['severeImpact'],[])
        
    def test_should_return_status_404_if_id_passed_to_get_method_is_invalid (self):
        url = "/api/v1/on-covid-19/100/"
        res = self.client.get(url)
        self.assertEqual(res.status_code,404)

    def test_put_method (self):
        url="/api/v1/on-covid-19/1/"
        res = self.client.get(url)
        # old_impact,old_severeImpact = res.data['impact'],res.data['severeImpact']

        new_data = {"name": "Changed_name",
                    "avgAge": 19.7,
                    "avgDailyIncomeInUSD": 5,
                    "avgDailyIncomePopulation": 0.71,
                    "periodType": "days",
                    "timeToElapse": 58,
                    "reportedCases": 674,
                    "population": 66622705,
                    "totalHospitalBeds": 1380614
                    }
        res=self.client.put(url,data=new_data)
        new_data.update({'id':1})
        self.assertEqual (res.data,new_data)
        # with self.subTest (res=res):
        #     self.assertEqual (res.data['impact'],old_impact)
        #     self.assertEqual (res.data['severeImpact'],old_severeImpact)
    
    def test_should_return_404_if_input_to_put_method_is_invalid (self):
        url = "/api/v1/on-covid-19/100/"
        res = self.client.get(url)
        # old_impact,old_severeImpact = res.data['impact'],res.data['severeImpact']

        new_data = {"name": "Changed_name",
                    "avgAge": 19.7,
                    "avgDailyIncomeInUSD": 5,
                    "avgDailyIncomePopulation": 0.71,
                    "periodType": "days",
                    "timeToElapse": 58,
                    "reportedCases": 674,
                    "population": 66622705,
                    "totalHospitalBeds": 1380614
                    }
        res=self.client.put(url,data=new_data)
        self.assertEqual (res.status_code,404)

    def test_should_check_that_id_of_input_isequal_to_that_of_impact_and_severeImpact (self):
        url = "/api/v1/on-covid-19/1/"
        res = self.client.get(url)

        self.assertEqual(res.data['input_data']['id'],1)
        self.assertEqual(res.data['impact']['id'],1)
        self.assertEqual(res.data['severeImpact']['id'],1)
        
    def test_delete_method (self):
        url = "/api/v1/on-covid-19/1/"
        res = self.client.delete(url)

        self.assertEqual (res.status_code,204)
        with self.subTest (url=url):
            res=self.client.get(url)
            self.assertEqual(res.status_code,404)

    def test_should_return_status_404_if_id_passed_to_delete_method_is_invalid (self):
        url = "/api/v1/on-covid-19/100/"
        res = self.client.delete(url)

        self.assertEqual(res.status_code, 404)
        
