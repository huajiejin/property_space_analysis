# Description: This file contains the API endpoints for the version 1 of the API.

import os
from typing import List
from ninja import NinjaAPI
from ninja.security import HttpBearer
from .schema_v1 import PropertySpaceIn, PropertySpaceOut, PatchPropertySpaceSchema
from api.models import Address, PropertySpace, UnitSpace, MeterData
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch, Q, Count
from django.http import Http404
from api.exceptions import ServiceUnavailableException
import logging


logger = logging.getLogger(__name__)


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        auth_token = os.getenv('AUTH_TOKEN')
        if token == auth_token:
            return token

api_v1 = NinjaAPI(version='1.0', auth=AuthBearer())


@api_v1.post("/property-spaces")
def create_property_space_v1(request, payload: PropertySpaceIn):
    logger.info(f"Creating property space: {payload.name}")
    address = Address.objects.create(
        street=payload.address.street,
        state=payload.address.state,
        city=payload.address.city,
        country=payload.address.country,
        postal_code=payload.address.postal_code
    )

    property_space = PropertySpace.objects.create(
        address=address,
        name=payload.name
    )
    logger.info(f"Property space created: {property_space.id}")
    return {"property_space_id": property_space.id}


@api_v1.get("/property-spaces/{property_space_id}", response=PropertySpaceOut)
def get_property_space_by_id_v1(request, property_space_id: int, year: int = None):
    logger.info(f"Getting property space by id: {property_space_id}")
    property_space = (
        PropertySpace.objects
        .filter(id=property_space_id)
        .select_related("address")
        .prefetch_related(_generate_property_space_prefetch(year))
    )
    if not property_space.exists():
        logger.error(f"Property space not found: {property_space_id}")
        raise Http404
    logger.info(f"Property space found: {property_space_id}")
    return _generate_property_space_dict(property_space.first())


@api_v1.get("/property-spaces", response=List[PropertySpaceOut])
def get_property_spaces_v1(request, year: int = None):
    logger.info(f"Getting all property spaces with year: {year}")
    property_spaces = (
        PropertySpace.objects
        .select_related("address")
        .prefetch_related(_generate_property_space_prefetch(year))
    )
    logger.info(f"Found {property_spaces.count()} property spaces")
    return [_generate_property_space_dict(property_space) for property_space in property_spaces]


@api_v1.put("/property-spaces/{property_space_id}")
def update_property_space_v1(request, property_space_id: int, payload: PatchPropertySpaceSchema):
    logger.info(f"Updating property space: {property_space_id}")
    property_space = get_object_or_404(PropertySpace, id=property_space_id)
    if payload.name:
        property_space.name = payload.name
    if payload.address:
        address = property_space.address
        for attr, value in payload.address.dict(exclude_unset=True).items():
            setattr(address, attr, value)
        address.save()
    property_space.save()
    logger.info(f"Property space updated: {property_space_id}")
    return {"success": True}


@api_v1.delete("/property-spaces/{property_space_id}")
def delete_property_space_v1(request, property_space_id: int):
    logger.info(f"Deleting property space: {property_space_id}")
    property_space = get_object_or_404(PropertySpace, id=property_space_id)
    property_space.delete()
    logger.info(f"Property space deleted: {property_space_id}")
    return {"success": True}


@api_v1.get("/service-unavailable-exception")
def simulate_service_unavailable_exception(request):
    raise ServiceUnavailableException("We are simulating a service unavailable exception.")


# custom exception handler
@api_v1.exception_handler(ServiceUnavailableException)
def service_unavailable(request, exc):
    logger.error(f"ServiceUnavailableException: {exc.message}")
    return api_v1.create_response(
        request,
        {"message": f'{exc.message} Please retry later'},
        status=503,
    )


def _generate_property_space_prefetch(year: int = None) -> Prefetch:
    """
    Generate a Prefetch object to be used in the PropertySpace queryset.
    This prefetch will optimize the queries to get the related data.

    Args:
        year (int): The year to filter the MeterData queryset.
    """
    meterdata_query = (
        MeterData.objects.all()
        .annotate(count=Count("unit_space"))
    )
    if year != None:
        meterdata_query = meterdata_query.filter(
            Q(measurement_start_date__year=year) | Q(measurement_end_date__year=year)
        )

    return Prefetch(
        "unitspace_set",
        queryset=UnitSpace.objects.prefetch_related(
            Prefetch(
                "meterdata_set",
                queryset=meterdata_query
            )
        )
    )


def _generate_property_space_dict(property_space: PropertySpace) -> PropertySpaceOut:
    """
    Generate a dictionary with the property space data.
    
    Args:
        property_space (PropertySpace): The property space object.
    """

    name = property_space.name
    address = property_space.address
    number_of_units = property_space.unitspace_set.count()
    total_area = sum(unit.area for unit in property_space.unitspace_set.all())
    # If a meter is shared between units, 
    #   the consumption of the meter will be divided by 
    #   the number of units associated with it.
    total_consumption = sum(
        meter.measurement_reading / meter.count 
        for unit in property_space.unitspace_set.all() 
        for meter in unit.meterdata_set.all()
    )
    # We are assuming that all meters have the same unit in the scope of the exercise.
    consumption_unit = "kWh"

    return {
        "name": name,
        "address": address,
        "number_of_units": number_of_units,
        "total_area": total_area,
        "total_consumption": total_consumption,
        "consumption_unit": consumption_unit
    }
