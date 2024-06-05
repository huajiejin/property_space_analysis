from django.http import JsonResponse
from django.views import View
from .models import PropertySpace, UnitSpace, MeterData

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
