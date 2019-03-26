from django.shortcuts import render

# Create your views here.

from rest_framework import generics
from .models import CarOBDData, CarJSONOBDData
from .serializers import CarOBDDataSerializer, CarJSONOBDDataSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json


# class ListCarsView(generics.ListAPIView):
#     """
#     Provides a get method handler.
#     """
#     queryset = CarProfile.objects.all()
#     serializer_class = CarSerializer

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
        serializer = CarOBDDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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