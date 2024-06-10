from django.test import TestCase
from api.models import PropertySpace
import os
import json

class ApiV1TestCase(TestCase):
    fixtures = ['api_testing_fixture.json']

    def setUp(self) -> None:
        self.client.defaults['HTTP_AUTHORIZATION'] = 'Bearer ' + os.getenv('AUTH_TOKEN')
        return super().setUp()

    def test_get_property_space_detail(self):
        response = self.client.get('/api/v1/property-spaces/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], "property space 1")
        self.assertEqual(response.json()['address']['street'], "123 Main St")
        self.assertEqual(response.json()['total_consumption'], 6000)
    
    def test_get_property_space_detail_with_year_2020(self):
        response = self.client.get('/api/v1/property-spaces/1?year=2020')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['total_consumption'], 0)
    
    def test_get_property_space_detail_with_year_2021(self):
        response = self.client.get('/api/v1/property-spaces/1?year=2021')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['total_consumption'], 1000)
    
    def test_get_property_space_detail_with_year_2022(self):
        response = self.client.get('/api/v1/property-spaces/1?year=2022')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['total_consumption'], 5000)

    def test_get_all_property_spaces(self):
        response = self.client.get('/api/v1/property-spaces')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)
        self.assertEqual(response.json()[0]['name'], "property space 1")
        self.assertEqual(response.json()[0]['address']['street'], "123 Main St")
        self.assertEqual(response.json()[0]['total_consumption'], 6000)
        self.assertEqual(response.json()[1]['name'], "property space 2")
        self.assertEqual(response.json()[1]['address']['street'], "456 Main St")
        self.assertEqual(response.json()[1]['total_consumption'], 7000)
        self.assertEqual(response.json()[2]['name'], "property space 3")
        self.assertEqual(response.json()[2]['address']['street'], "789 Main St")
        self.assertEqual(response.json()[2]['total_consumption'], 8000)
    
    def test_get_all_property_spaces_with_year_2020(self):
        response = self.client.get('/api/v1/property-spaces?year=2020')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]['total_consumption'], 0)
        self.assertEqual(response.json()[1]['total_consumption'], 0)
        self.assertEqual(response.json()[2]['total_consumption'], 0)
    
    def test_get_all_property_spaces_with_year_2021(self):
        response = self.client.get('/api/v1/property-spaces?year=2021')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]['total_consumption'], 1000)
        self.assertEqual(response.json()[1]['total_consumption'], 0)
        self.assertEqual(response.json()[2]['total_consumption'], 0)
    
    def test_get_all_property_spaces_with_year_2022(self):
        response = self.client.get('/api/v1/property-spaces?year=2022')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]['total_consumption'], 5000)
        self.assertEqual(response.json()[1]['total_consumption'], 3000)
        self.assertEqual(response.json()[2]['total_consumption'], 3000)
    
    def test_get_all_property_spaces_with_year_2023(self):
        response = self.client.get('/api/v1/property-spaces?year=2023')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]['total_consumption'], 0)
        self.assertEqual(response.json()[1]['total_consumption'], 4000)
        self.assertEqual(response.json()[2]['total_consumption'], 0)

    def test_get_all_property_spaces_with_year_2024(self):
        response = self.client.get('/api/v1/property-spaces?year=2024')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]['total_consumption'], 0)
        self.assertEqual(response.json()[1]['total_consumption'], 0)
        self.assertEqual(response.json()[2]['total_consumption'], 5000)
    
    def test_post_property_space(self):
        response = self.client.post('/api/v1/property-spaces',
                                    data=json.dumps({
                                        "name": "New Space", 
                                        "address": {
                                            "street": "246 Main St",
                                            "city": "San Francisco",
                                            "state": "CA",
                                            "country": "USA",
                                            "postal_code": "94105",
                                        }
                                    }),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(PropertySpace.objects.filter(name="New Space").exists())

    def test_put_property_space(self):
        property_space_1_response = self.client.get('/api/v1/property-spaces/1')
        self.assertFalse(property_space_1_response.json()['name'] == "Updated Space")
        response = self.client.put('/api/v1/property-spaces/1',
                                    data=json.dumps({"name": "Updated Space"}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        property_space_1_response = self.client.get('/api/v1/property-spaces/1')
        self.assertEqual(property_space_1_response.json()['name'], "Updated Space")

    def test_delete_property_space(self):
        property_space_1_response = self.client.get('/api/v1/property-spaces/1')
        self.assertTrue(property_space_1_response.json())
        response = self.client.delete('/api/v1/property-spaces/1')
        self.assertEqual(response.status_code, 200)
        self.client.get('/api/v1/property-spaces/1')
        property_space_1_response = self.client.get('/api/v1/property-spaces/1')
        self.assertEqual(property_space_1_response.status_code, 404)
