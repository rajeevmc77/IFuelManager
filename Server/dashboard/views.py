from django.shortcuts import render

from django.http import HttpResponse
from django.views import View
from django.db.models import  Avg, Sum, StdDev

from obdService.models import CarOBDData, CarProfile
# Create your views here.

class DashboardView(View):
    def get(self, request):
        carOBDData = CarOBDData.objects.values('VIN').annotate(Avg('FuelUsageDeviation'))
        #CarOBDData.objects.aggregate(Avg('FuelUsageDeviation'))

        return render(request, "dashboard/dashboard.html",
                      { 'CarOBDData': CarOBDData.objects.all(), 'CarProfile': CarProfile.objects.all() })