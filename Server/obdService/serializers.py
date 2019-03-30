from rest_framework import serializers
from .models import CarOBDData


class CarOBDDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarOBDData
        fields = ("VIN", "Speed", "RPM", "FuelTankLevel","FuelUsageTrend" ) # , "SecondsElapsed")


