from django.shortcuts import render

from django.http import HttpResponse
from django.views import View
from django.db.models import  Avg, Sum, StdDev

from obdService.models import CarOBDData, CarProfile
# Create your views here.

class DashboardView(View):
    def get(self, request):
        carsWithSpuriousHistory = CarOBDData.objects.values('VIN').filter(PossibleFuelLeak=1).distinct()
        carsWithCleanHistry = CarOBDData.objects.values('VIN').exclude(VIN__in=carsWithSpuriousHistory).distinct()
        carProfiles = list(CarProfile.objects.all())
        carHistoryProfile = dict()
        carsHistry= list()
        carsHistry.append([dict(item,**{'PossibleFuelLeak':0}) for item in carsWithCleanHistry])
        carsHistry.append([dict(item, **{'PossibleFuelLeak': 1}) for item in carsWithSpuriousHistory])

        for item in carsHistry:
            for profile in carProfiles:
                if profile.VIN == item[0]["VIN"]:
                    item[0].update({"Make": profile.Make, "Model": profile.Model})
                    break

        return render(request, "dashboard/dashboard.html",
                      { 'CarOBDData': CarOBDData.objects.all(),
                        'CarProfile': CarProfile.objects.all(),
                        'CarHistory': carsHistry
                      })