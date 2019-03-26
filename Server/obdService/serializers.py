from rest_framework import serializers
from .models import CarOBDData, CarJSONOBDData


class CarOBDDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarOBDData
        fields = ("VIN", "Speed", "RPM", "FuelTankLevel")

class CarJSONOBDDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarJSONOBDData
        fields = ("Speed", "RPM","VIN")
