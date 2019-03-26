from django.shortcuts import render

from django.http import HttpResponse
from django.views import View

from obdService.models import CarOBDData
# Create your views here.

class DashboardView(View):
    def get(self, request):
        # <view logic>
        return render(request, "dashboard/dashboard.html",
                      { 'CarOBDData': CarOBDData.objects.all()})