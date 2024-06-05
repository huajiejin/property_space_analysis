from django.test import TestCase

class PropertySpaceViewTestCase(TestCase):
    fixtures = ['api_testing_fixture.json']

    def test_property_space_view_load(self):
        response = self.client.get('/api/property-space/')
        self.assertEqual(response.status_code, 200)

    def test_property_space_view_response_length(self):
        response = self.client.get('/api/property-space/')
        self.assertEqual(len(response.json()), 3)
