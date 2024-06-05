# Description: Schema for PropertySpace endpoints
from ninja import Schema, ModelSchema, Field
from api.models import PropertySpace

class AddressSchema(Schema):
	street: str = Field(min_length=2, max_length=64)
	city: str = Field(min_length=2, max_length=64)
	state: str = Field(min_length=2, max_length=64)
	country: str = Field(min_length=2, max_length=64)
	postal_code: str = Field(min_length=2, max_length=64)

class PropertySpaceIn(Schema):
	name: str = Field(min_length=2, max_length=128)
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
