from django.db import models

# Create your models here.


class CarProfile(models.Model):
    class Meta:
        verbose_name = 'CarProfile'
        verbose_name_plural = 'CarProfile'

    # car Vehicle Identification Number
    VIN = models.CharField(max_length=20, null=False, default="ABC123")
    # Car Owner First Name
    OwnerFirstName = models.CharField(max_length=50, null=False, default="Rajeev")
    # Car Owner Last Name
    OwnerLastName = models.CharField(max_length=50, null=False, default="M C ")
    # car Make
    Make = models.CharField(max_length=50, null=False, default="Renault")
    # car Model
    Model = models.CharField(max_length=50, null=False, default="Duster")
    # Fuel Tank Volume
    FuelTankVolume = models.IntegerField(null=False, default=0)

    def __str__(self):
        return "{} - {} - {}  - {} - {} ".format(self.VIN, self.OwnerFirstName, self.OwnerLastName, self.Make,
                                                 self.Model)

class CarOBDData(models.Model):
    class Meta:
        verbose_name = 'CarOBDData'
        verbose_name_plural = 'CarOBDData'
    # car Vehicle Identification Number
    VIN = models.CharField(max_length=20, null=False, default="ABC123")
    # Car RPM
    RPM = models.IntegerField(null=False,default=0)
    # car Speed
    Speed = models.FloatField(null=False, default=0)
    # Fuel Level 0 - 100 %
    FuelTankLevel = models.FloatField(null=False, default=0)
    # User Profile
    # profile = models.ForeignKey(CarProfile, on_delete=models.CASCADE, default=1)
    # object created Time
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    # object updated Time
    #updated_at = models.DateTimeField(auto_now=True, blank=True)
    #usage Trend for the last 10 samples
    FuelUsageTrend = models.FloatField(null=False, default=0)
    # seconds Elapsed from Last Read
    # SecondsElapsed = models.FloatField(null=False, default=1)
    FuelUsageDeviation = models.FloatField(null=False, default=0)


    def __str__(self):
        return "{} - {} - {}  - {}".format(self.VIN, self.RPM, self.Speed, self.FuelTankLevel)

