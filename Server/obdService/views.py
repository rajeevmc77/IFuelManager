from django.shortcuts import render

# Create your views here.

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
import datetime as dt
import pytz
from scipy.stats import linregress
import statistics

from .models import CarOBDData,  CarProfile
from .serializers import CarOBDDataSerializer

class CarOBDDataView(APIView):
    """
    API to capture OBD Data from vehicle
    """

    def get(self, request, format=None):
        """

        """
        carprofiles = CarOBDData.objects.all()
        serializer = CarOBDDataSerializer(carprofiles, many=True)
        return Response(serializer.data)

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

    def setFuelUsageTrend(self, data):
        """
               Normalize the Fuel level Data receiced from Vehicle. Make Necessory Adjustments
               Author: Akshara Gireesh Murali
        """
        fuelreadingSamples = CarOBDData.objects.filter(VIN=data['VIN']).values_list('FuelTankLevel', 'id',
                                    'FuelUsageTrend').order_by('-created_at')[:10]
        if fuelreadingSamples:
            fuelTankLevel =  [item[0] for item in fuelreadingSamples ] #list(fuelreadingSamples)
            sampleID = [item[1] for item in fuelreadingSamples]
            usageDeviation = [item[2] for item in fuelreadingSamples if item[2] < 0 ]
            if len(usageDeviation) >=2 :
                fuelUsageDeviation = statistics.stdev(usageDeviation)
            else:
                fuelUsageDeviation=0
            fuelUsageTrend = linregress(sampleID, fuelTankLevel)
        else :
            fuelUsageTrend = None
            fuelUsageDeviation = None
        if fuelUsageTrend:
            if fuelUsageTrend.slope == fuelUsageTrend.slope:
                data['FuelUsageTrend'] = fuelUsageTrend.slope * 10000
        if fuelUsageDeviation:
            data['FuelUsageDeviation']= fuelUsageDeviation
        return data

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
            projectedRemainingFuel = previousReading - ((0.005 * adjustmentMultiplier * secondsElapsed)/ fuelTankVolume)
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
            data["PossibleFuelLeak"] = 1 if (lastfuelTankLevel - data["FuelTankLevel"]) > 0.01 else 0
        return data
