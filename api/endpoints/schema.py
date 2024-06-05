from datetime import date
from ninja import Schema, ModelSchema
from api.models import PropertySpace

class AddressSchema(Schema):
	street: str
	city: str
	state: str
	country: str
	postal_code: str

class PropertySpaceIn(Schema):
	name: str
	address: AddressSchema

class PatchPropertySpaceSchema(ModelSchema):
    class Meta:
        model = PropertySpace
        fields = ['name', 'address']
        fields_optional = '__all__'

class PropertySpaceOut(Schema):
	name: str
	address: AddressSchema
	number_of_units: int
	total_area: float
	total_consumption: float
	consumption_unit: str
