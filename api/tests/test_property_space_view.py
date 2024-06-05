from django.test import TestCase
from api.models import PropertySpace
import json

class PropertySpaceViewTestCase(TestCase):
    fixtures = ['api_testing_fixture.json']

    def test_property_space_view_load(self):
        response = self.client.get('/api/property-space/')
        self.assertEqual(response.status_code, 200)

    def test_property_space_view_response_length(self):
        response = self.client.get('/api/property-space/')
        self.assertEqual(len(response.json()), 3)
    
    def test_post_property_space(self):
        response = self.client.post('/api/property-space/',
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
        self.assertEqual(response.status_code, 201)
        self.assertTrue(PropertySpace.objects.filter(name="New Space").exists())

    def test_put_property_space(self):
        property_space_1_response = self.client.get('/api/property-space/1/')
        self.assertFalse(property_space_1_response.json()[0]['name'] == "Updated Space")
        response = self.client.put('/api/property-space/1/',
                                    data=json.dumps({"name": "Updated Space"}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        property_space_1_response = self.client.get('/api/property-space/1/')
        self.assertEqual(property_space_1_response.json()[0]['name'], "Updated Space")

    def test_delete_property_space(self):
        property_space_1_response = self.client.get('/api/property-space/1/')
        self.assertTrue(property_space_1_response.json())
        response = self.client.delete('/api/property-space/1/')
        self.assertEqual(response.status_code, 200)
        self.client.get('/api/property-space/1/')
        property_space_1_response = self.client.get('/api/property-space/1/')
        self.assertEqual(property_space_1_response.status_code, 404)
