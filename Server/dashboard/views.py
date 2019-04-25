from django.shortcuts import render

from django.http import HttpResponse
from django.views import View
from django.db.models import  Avg, Sum, StdDev, Max, Min
import json
import json
from django.core.serializers.json import DjangoJSONEncoder

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
                        'CarFuelHistory': carsHistry,
                        'jsonCarFuelHistory' : json.dumps(carsHistry)
                      })

    def chartView(request):
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

    def adminView(request):

        return render(request, "dashboard/AdminView.html",
                      {
                      })

    def resetFuelData(request):
        vin = None
        carObdReading = None
        carProfile = None
        jsonCarProfile = None
        if request.method == 'GET' and 'vin' in request.GET:
            vin = request.GET['vin']
        if vin is not None:
            CarOBDData.objects.filter(VIN=vin).update(PossibleFuelLeak=0)
            return HttpResponse(json.dumps("{'ResetStatus':'Success'}"), content_type="application/json")
        else:
            return HttpResponse(json.dumps("{'ResetStatus':'Failed'}"), content_type="application/json")
        #http://localhost:8000/dashboard/resetFuelLevel/?vin=MAKDF665JJ4003504
        #return HttpResponse(json.dumps(response_data), content_type="application/json")
        #return HttpResponse("Reset Done.")

    def getAjaxFuelData(request):
        vin = None
        carObdReading = None
        carProfile = None
        jsonCarProfile = None
        if request.method == 'GET' and 'vin' in request.GET:
            vin = request.GET['vin']
        if vin is not None:
            carObdReading = list(CarOBDData.objects.filter(VIN=vin).values_list('id', 'FuelTankLevel').order_by('-created_at')[:50])
            carObdReading = json.dumps(carObdReading)
            return HttpResponse(carObdReading, content_type="application/json")
        else:
            return HttpResponse(json.dumps("{'ResetStatus':'Failed'}"), content_type="application/json")
        #http://localhost:8000/dashboard/getFuelHistory/?vin=MAKDF665JJ4003504

    def getAjaxHistoryRange(request):
        vin = None
        carObdReading = None
        if request.method == 'GET' and 'vin' in request.GET:
            vin = request.GET['vin']
        if vin is not None:
            max_id = CarOBDData.objects.all().aggregate(Max('id'))['id__max']
            min_id = CarOBDData.objects.all().aggregate(Min('id'))['id__min']
            retval = {"MinID": min_id, "MaxID": max_id}
            retval = json.dumps(retval)
            return HttpResponse(retval, content_type="application/json")
        else:
            return HttpResponse(json.dumps("{'ResetStatus':'Failed'}"), content_type="application/json")
        # http://localhost:8000/dashboard/getHistoryRange/?vin=MAKDF665JJ4003504

    def getAjaxHistoryInRange(request):
        vin = None
        fromId = None
        toId = None
        carObdReading = None
        if request.method == 'GET' and 'vin' in request.GET and 'fromID' in request.GET and 'toId' in request.GET:
            vin = request.GET['vin']
            fromID = int(request.GET['fromID'])
            toId = int(request.GET['toId'])
        if vin is not None and fromID is not None and toId is not None:
            retval = list(CarOBDData.objects.values_list('id', 'FuelTankLevel','created_at').filter(id__range=(fromID, toId)).order_by('created_at'))
            retval = json.dumps(retval, cls=DjangoJSONEncoder)
            return HttpResponse(retval, content_type="application/json")
        else:
            return HttpResponse(json.dumps("{'ResetStatus':'Failed'}"), content_type="application/json")
        # http://localhost:8000/dashboard/getHistoryInRange/?vin=MAKDF665JJ4003504&fromID=1&toId=50