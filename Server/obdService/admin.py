from django.contrib import admin
from .models import CarOBDData, CarProfile

# Register your models here.

admin.site.site_header = "iFuel Manager "
admin.site.site_title = "iFuel Manager"

admin.site.register(CarOBDData)
admin.site.register(CarProfile)
