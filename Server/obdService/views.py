from django.shortcuts import render

# Create your views here.

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
import datetime as dt
import pytz

from .models import CarOBDData,  CarProfile
from .serializers import CarOBDDataSerializer

class CarOBDDataView(APIView):
    """
    API to capture OBD Data from vehicle
    """

    def get(self, request, format=None):
        """
            API to get the data to populate the Dashboard
            Author : Akshara Gireesh Murali
        """
        carsWithSpuriousHistory = CarOBDData.objects.values('VIN').filter(PossibleFuelLeak=1).distinct()
        carsWithCleanHistry = CarOBDData.objects.values('VIN').exclude(VIN__in=carsWithSpuriousHistory).distinct()
        carProfiles = list(CarProfile.objects.all())

        carsHistry = [dict(item, **{'PossibleFuelLeak': 0}) for item in carsWithCleanHistry]
        carsHistry = carsHistry + [dict(item, **{'PossibleFuelLeak': 1}) for item in carsWithSpuriousHistory]

        for item in carsHistry:
            carLastDashboardReading = CarOBDData.objects.filter(VIN=item["VIN"]).values_list('FuelTankLevel',
                                                                                             'RPM', 'Speed').order_by(
                '-created_at')[:1]
            for profile in carProfiles:
                if profile.VIN == item["VIN"]:
                    item.update({"Make": profile.Make, "Model": profile.Model})
                    if carLastDashboardReading and len(carLastDashboardReading) > 0:
                        item["dashboard"] = {'FuelTankLevel': carLastDashboardReading[0][0],
                                             'RPM': carLastDashboardReading[0][1],
                                             'Speed': carLastDashboardReading[0][2]}
                    break
        return Response(json.dumps(carsHistry))

    def post(self, request, format=None):
        data = self.getJSON(request)
        data = self.setFuelLevelData(data)
        #data = self.setFuelUsageTrend(data)
        data = self.setFuelUsageSpikes(data)
        serializer = CarOBDDataSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def getJSON(self,request):
        jsondata = request.body.decode("utf-8").rstrip('\x00')
        data = json.loads(jsondata)
        return  data

    def setFuelLevelData(self,data):
        """
        Normalize the Fuel level Data receiced from Vehicle. Make Necessory Adjustments
        Author: Akshara Gireesh Murali
        """
        previousReading = CarOBDData.objects.filter(VIN=data['VIN']).values_list('FuelTankLevel','created_at').order_by('-created_at')[:1]
        if not previousReading:
            previousReading = 81
            lastKnownReadTime = dt.datetime.now()
        else:
            lastKnownReadTime = previousReading[0][1]
            previousReading = previousReading[0][0]
        fuelTankVolume = CarProfile.objects.filter(VIN=data['VIN']).values_list('FuelTankVolume')
        if not fuelTankVolume:
            fuelTankVolume = 35
        else:
            fuelTankVolume= fuelTankVolume[0][0]
        if not lastKnownReadTime:
            projectedRemainingFuel = previousReading - (0.005 / fuelTankVolume)
            secondsElapsed = 0
        else:
            utc = pytz.UTC
            now = utc.localize(dt.datetime.now())
            if not lastKnownReadTime.tzinfo:
                lastKnownReadTime=utc.localize(lastKnownReadTime)
            secondsElapsed = (now - lastKnownReadTime ).total_seconds()
            adjustmentMultiplier = 0
            if secondsElapsed < 60:
                adjustmentMultiplier = 1
            projectedRemainingFuel = previousReading - ((0.0005 * adjustmentMultiplier * secondsElapsed)/ fuelTankVolume)
        if int(data['FuelTankLevel']) == 0:
            data['FuelTankLevel'] = projectedRemainingFuel
        return data

    def setFuelUsageSpikes(self, data):
        """
               Normalize the Fuel level Data receiced from Vehicle. Make Necessory Adjustments
               Author: Akshara Gireesh Murali
        """
        fuelreadingSamples = CarOBDData.objects.filter(VIN=data['VIN']).values_list('FuelTankLevel').order_by('-created_at')[:1]
        if fuelreadingSamples:
            lastfuelTankLevel = fuelreadingSamples[0][0]
            data["PossibleFuelLeak"] = 1 if (lastfuelTankLevel - float(data["FuelTankLevel"])) > 0.01 else 0
        return data
