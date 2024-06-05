# Definition of the models using Django ORM

from django.db import models

class Address(models.Model):
    street = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=64)
    country = models.CharField(max_length=64)
    postal_code = models.CharField(max_length=64)

class PropertySpace(models.Model):
    name = models.CharField(max_length=128)
    address = models.OneToOneField(
        Address,
        on_delete=models.CASCADE,
    )

class UnitSpace(models.Model):
    UNIT_TYPE_CHOICES = [
        ('COMMON_AREA', 'Common Area'),
        ('VACANT', 'Vacant'),
        ('LEASED', 'Leased'),
    ]

    name = models.CharField(max_length=128)
    unit_type = models.CharField(max_length=32, choices=UNIT_TYPE_CHOICES, default='COMMON_AREA')
    area = models.FloatField()
    property_space = models.ForeignKey(
        PropertySpace,
        on_delete=models.CASCADE,
    )

class MeterData(models.Model):
    UNIT_CHOICES = [
        ('kWh', 'kWh'),
        ('therms', 'Therms'),
    ]

    meter_number = models.CharField(max_length=128)
    meter_provider_name = models.CharField(max_length=128)
    meter_source = models.CharField(max_length=128)
    measurement_reading = models.FloatField()
    measurement_unit = models.CharField(max_length=32, choices=UNIT_CHOICES, default='kWh')
    measurement_start_date = models.DateTimeField()
    measurement_end_date = models.DateTimeField()
    unit_space = models.ManyToManyField(UnitSpace)

    def __str__(self):
        return "%s (%s)" % (
            self.meter_provider_name,
            ", ".join(unit_space.name for unit_space in self.unit_space.all()),
        )
