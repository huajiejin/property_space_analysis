from django.http import JsonResponse
from django.views import View
from .models import Address, PropertySpace, UnitSpace, MeterData
import json
from django.shortcuts import get_object_or_404

class PropertySpaceView(View):
    def get(self, request, *args, **kwargs):
        if kwargs.get('id'):
            return self.__get_property_space_detail(kwargs['id'])
        else:
            return self.__get_all_property_spaces()

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        address_data = data.pop('address')
        address = Address.objects.create(**address_data)
        space = PropertySpace.objects.create(address=address, **data)
        return JsonResponse({"id": space.id}, status=201)

    def put(self, request, *args, **kwargs):
        space = get_object_or_404(PropertySpace, pk=kwargs['id'])
        data = json.loads(request.body)
        for key, value in data.items():
            setattr(space, key, value)
        space.save()
        return JsonResponse({"id": space.id})

    def delete(self, request, *args, **kwargs):
        space = get_object_or_404(PropertySpace, pk=kwargs['id'])
        space.delete()
        return JsonResponse({"detail": "Deleted successfully"})
    
    def __get_property_space_detail(self, id):
        space = get_object_or_404(PropertySpace, pk=id)
        space_json = self.__create_json_from_property_space(space)
        return JsonResponse({"property_space": space_json})

    def __get_all_property_spaces(self):
        data = []
        spaces = PropertySpace.objects.all()

        for space in spaces:
            space_json = self.__create_json_from_property_space(space)
            data.append(space_json)

        return JsonResponse({"all_property_spaces": data})

    def __create_json_from_property_space(self, space):
        units = UnitSpace.objects.filter(property_space=space)
        meters = MeterData.objects.filter(unit_space__in=units)
        return {
            "name": space.name,
            "address": {
                "street": space.address.street,
                "city": space.address.city,
                "state": space.address.state,
                "country": space.address.country,
                "postal_code": space.address.postal_code,
            },
            "number_of_units": units.count(),
            "total_area": sum(unit.area for unit in units),
            "total_consumption": sum(meter.measurement_reading for meter in meters),
            "consumption_unit": "kWh" if meters else None,
        }
