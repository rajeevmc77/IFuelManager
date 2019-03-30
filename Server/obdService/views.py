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

from .models import CarOBDData,  CarProfile
from .serializers import CarOBDDataSerializer

class CarOBDDataView(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    """

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        carprofiles = CarOBDData.objects.all()
        serializer = CarOBDDataSerializer(carprofiles, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):

        data = self.getJSON(request)
        if int(data['FuelTankLevel']) == 0:
            remainingFuelData = self.getProjectedRemainingFuel(data)
            data['FuelTankLevel'] = remainingFuelData[0]
            data['SecondsElapsed'] = remainingFuelData[1] if remainingFuelData[1] > 1 else 1
            trendinputData = {'VIN': data['VIN'],'FuelTankLevel': remainingFuelData[0], 'SecondsElapsed': remainingFuelData[1]}
            trend = self.getFuelUsageTrend(trendinputData)
            if trend:
                if trend.slope == trend.slope:
                    print(trend.slope)
                    data['FuelUsageTrend'] = trend.slope * 10000
        serializer = CarOBDDataSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def getJSON(self,request):
        jsondata = request.body.decode("utf-8").rstrip('\x00')
        data = json.loads(jsondata)
        return  data

    def getFuelUsageTrend(self, data):
        fuelreadingSamples = CarOBDData.objects.filter(VIN=data['VIN']).filter( SecondsElapsed__lte = 59 ,
            SecondsElapsed__gte=1).values_list('FuelTankLevel', 'SecondsElapsed').order_by('-created_at')[:10]
        if fuelreadingSamples:
            fuelTankLevel =  [item[0] for item in fuelreadingSamples ] #list(fuelreadingSamples)
            elapsedTimeFromLastRead = [item[1] for item in fuelreadingSamples]
            fuelUsageTrend = linregress(elapsedTimeFromLastRead, fuelTankLevel)
        else :
            fuelUsageTrend = None
        return fuelUsageTrend




    def getProjectedRemainingFuel(self,data):
        previousReading = CarOBDData.objects.filter(VIN=data['VIN']).values_list('FuelTankLevel','created_at').order_by('-created_at')[:1]
        if not previousReading:
            previousReading = 81
            lastKnownReadTime = dt.datetime.now()
        else:
            #print (data['created_at'])
            lastKnownReadTime = previousReading[0][1]
            previousReading = previousReading[0][0]

        fuelTankVolume = CarProfile.objects.filter(VIN=data['VIN']).values_list('FuelTankVolume')
        if not fuelTankVolume:
            fuelTankVolume = 35
        else:
            fuelTankVolume= fuelTankVolume[0][0]

        if not lastKnownReadTime:
            projectedRemainingFuel = previousReading - (0.005 / fuelTankVolume)
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
        return ( projectedRemainingFuel, secondsElapsed )

