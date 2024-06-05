import os
from typing import List
from ninja import NinjaAPI
from ninja.security import HttpBearer
from .schema import PropertySpaceIn, PropertySpaceOut, PatchPropertySpaceSchema
from api.models import Address, PropertySpace, UnitSpace, MeterData
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch, Q
from django.http import Http404


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        auth_token = os.getenv('AUTH_TOKEN')
        if token == auth_token:
            return token

api_v1 = NinjaAPI(version='1.0', auth=AuthBearer())


@api_v1.post("/property-spaces")
def create_property_space_v1(request, payload: PropertySpaceIn):
    address = Address.objects.create(
        street=payload.address.street,
        state=payload.address.state,
        country=payload.address.country,
        postal_code=payload.address.postal_code
    )
    property_space = PropertySpace.objects.create(
        address=address,
        name=payload.name
    )
    return {"property_space_id": property_space.id}


@api_v1.get("/property-spaces/{property_space_id}", response=PropertySpaceOut)
def get_property_space_by_id_v1(request, property_space_id: int, year: int = None):
    if year:
        property_space = PropertySpace.objects.filter(id=property_space_id).prefetch_related(
            Prefetch(
                "unitspace_set",
                queryset=UnitSpace.objects.prefetch_related(
                    Prefetch(
                        "meterdata_set",
                        queryset=MeterData.objects.filter(
                            Q(measurement_start_date__year=year) | Q(measurement_end_date__year=year)
                        )
                    )
                )
            )
        )
    else:
        property_space = PropertySpace.objects.filter(id=property_space_id).prefetch_related(
            Prefetch(
                "unitspace_set",
                queryset=UnitSpace.objects.prefetch_related("meterdata_set")
            )
        )
    if not property_space.exists():
        raise Http404
    return _generate_property_space_dict(property_space.first())


@api_v1.get("/property-spaces", response=List[PropertySpaceOut])
def get_property_spaces_v1(request, year: int = None):
    if year:
        property_spaces = PropertySpace.objects.prefetch_related(
            Prefetch(
                "unitspace_set",
                queryset=UnitSpace.objects.prefetch_related(
                    Prefetch(
                        "meterdata_set",
                        queryset=MeterData.objects.filter(
                            Q(measurement_start_date__year=year) | Q(measurement_end_date__year=year)
                        )
                    )
                )
            )
        )
    else:
        property_spaces = PropertySpace.objects.prefetch_related(
            Prefetch(
                "unitspace_set",
                queryset=UnitSpace.objects.prefetch_related("meterdata_set")
            )
        )
    return [_generate_property_space_dict(property_space, ) for property_space in property_spaces]


@api_v1.put("/property-spaces/{property_space_id}")
def update_property_space_v1(request, property_space_id: int, payload: PatchPropertySpaceSchema):
    property_space = get_object_or_404(PropertySpace, id=property_space_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(property_space, attr, value)
    property_space.save()
    return {"success": True}


@api_v1.delete("/property-spaces/{property_space_id}")
def delete_property_space_v1(request, property_space_id: int):
    property_space = get_object_or_404(PropertySpace, id=property_space_id)
    property_space.delete()
    return {"success": True}


def _generate_property_space_dict(property_space) -> PropertySpaceOut:
    return {
        "name": property_space.name,
        "address": {
            "street": property_space.address.street,
            "city": property_space.address.city,
            "state": property_space.address.state,
            "country": property_space.address.country,
            "postal_code": property_space.address.postal_code,
        },
        "number_of_units": property_space.unitspace_set.count(),
        "total_area": sum(unit.area for unit in property_space.unitspace_set.all()),
        # If a meter is shared between units, it will be counted multiple times.
        "total_consumption": sum(meter.measurement_reading for unit in property_space.unitspace_set.all() for meter in unit.meterdata_set.all()),
        # We are assuming that all meters have the same unit in the scope of the exercise.
        "consumption_unit": "kWh"
    }
