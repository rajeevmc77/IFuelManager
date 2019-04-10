from django.shortcuts import render

from django.http import HttpResponse
from django.views import View
from django.db.models import  Avg, Sum, StdDev
import json

from obdService.models import CarOBDData, CarProfile
# Create your views here.

class DashboardView(View):
    def get(self, request):
        carsWithSpuriousHistory = CarOBDData.objects.values('VIN').filter(PossibleFuelLeak=1).distinct()
        carsWithCleanHistry = CarOBDData.objects.values('VIN').exclude(VIN__in=carsWithSpuriousHistory).distinct()
        carProfiles = list(CarProfile.objects.all())

        carsHistry = [dict(item,**{'PossibleFuelLeak':0}) for item in carsWithCleanHistry]
        carsHistry = carsHistry + [dict(item, **{'PossibleFuelLeak': 1}) for item in carsWithSpuriousHistory]

        for item in carsHistry:
            carLastDashboardReading = CarOBDData.objects.filter(VIN=item["VIN"]).values_list('FuelTankLevel',
                                      'RPM', 'Speed').order_by('-created_at')[:1]
            for profile in carProfiles:
                if profile.VIN == item["VIN"]:
                    item.update({"Make": profile.Make, "Model": profile.Model})
                    if carLastDashboardReading  and len(carLastDashboardReading) > 0 :
                        item["dashboard"] = {'FuelTankLevel': carLastDashboardReading[0][0], 'RPM': carLastDashboardReading[0][1],
                                             'Speed': carLastDashboardReading[0][2]}
                    break

        return render(request, "dashboard/dashboard.html",
                      {
                        #'CarOBDData': CarOBDData.objects.all(),
                        'CarFuelHistory': carsHistry,
                        'jsonCarFuelHistory' : json.dumps(carsHistry)
                      })

    def chartView(request):
        # http://localhost:8000/dashboard/chartView/?vin=123
        # request.GET['vin']
        vin = None
        carObdReading = None
        carProfile = None
        jsonCarProfile = None
        if request.method == 'GET' and 'vin' in request.GET:
            vin = request.GET['vin']

        if vin is not None:
            carObdReading = list(CarOBDData.objects.filter(VIN = vin).values_list('id','FuelTankLevel').order_by('-created_at')[:50])
            carObdReading = json.dumps(carObdReading)
            carProfile = CarProfile.objects.filter(VIN = vin).values('OwnerFirstName', 'OwnerLastName', 'Make', 'Model', 'VIN')
            jsonCarProfile = json.dumps(list(carProfile))

        return render(request, "dashboard/FuelChart.html",
                      {
                          # 'CarOBDData': CarOBDData.objects.all(),
                          'carObdReading': carObdReading,
                          'carProfile': carProfile,
                          'jsonCarProfile': jsonCarProfile
                      })
