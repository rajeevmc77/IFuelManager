from django.shortcuts import render

# Create your views here.

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json

from .models import CarOBDData, CarJSONOBDData, CarProfile
from .serializers import CarOBDDataSerializer, CarJSONOBDDataSerializer

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
        print('data')
        print(data)
        if data['FuelTankLevel'] == 0:
            data['FuelTankLevel'] = self.getProjectedRemainingFuel(data)
        serializer = CarOBDDataSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def getJSON(self,request):
        jsondata = request.body.decode("utf-8").rstrip('\x00')
        data = json.loads(jsondata)
        return  data


    def getProjectedRemainingFuel(self,data):
        projectedRemainingFuel = 85
        previousReading = CarOBDData.objects.filter(VIN=data['VIN']).values_list('FuelTankLevel').order_by('-created_at')[:1];
        if not previousReading:
            previousReading = 81
        else:
            previousReading = previousReading[0][0]
        fuelTankVolume = CarProfile.objects.filter(VIN=data['VIN']).values_list('FuelTankVolume')
        if not fuelTankVolume:
            fuelTankVolume = 35
        else:
            fuelTankVolume= fuelTankVolume[0][0]
        projectedRemainingFuel = previousReading - (0.005/ fuelTankVolume)

        return projectedRemainingFuel

class CarJSONOBDDataView(APIView):
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
        carprofiles = CarJSONOBDData.objects.all()
        serializer = CarJSONOBDDataSerializer(carprofiles, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        print(request.body);
        # print(request.data);
        print(request.body.decode("utf-8").rstrip('\x00'));
        jsondata = request.body.decode("utf-8").rstrip('\x00')
        d = json.loads(jsondata)
        serializer = CarJSONOBDDataSerializer(data=d)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        #return Response(serializer.data, status=status.HTTP_201_CREATED)