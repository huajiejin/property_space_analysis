from django.http import JsonResponse
from django.views import View
from .models import Address, PropertySpace, UnitSpace, MeterData
import json
from django.shortcuts import get_object_or_404

class PropertySpaceView(View):
    def get(self, request, *args, **kwargs):
        data = []
        if kwargs.get('id'):
            spaces = [PropertySpace.objects.get(pk=kwargs['id'])]
        else:
            spaces = PropertySpace.objects.all()

        for space in spaces:
            units = UnitSpace.objects.filter(property_space=space)
            meters = MeterData.objects.filter(unit_space__in=units)
            data.append({
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
            })

        return JsonResponse(data, safe=False)

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
