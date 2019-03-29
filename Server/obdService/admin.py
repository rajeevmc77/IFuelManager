from django.contrib import admin
from .models import CarOBDData, CarProfile

# Register your models here.

admin.site.register(CarOBDData)
admin.site.register(CarProfile)
