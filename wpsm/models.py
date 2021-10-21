from django.db import models
from datetime import datetime

# Create your models here.
class FP(models.Model):
    latitude = models.FloatField('latitude')
    longitude = models.FloatField('longitude')
    provider = models.CharField('provider', max_length=10)
    accuracy = models.FloatField('accuracy')
    app_name = models.CharField('app name that is gathering', max_length=50)
    location_name = models.CharField(max_length=30)
    reg_date = models.DateField('date published', default=datetime.today)


class ScanMac(models.Model):
    fp_id = models.ForeignKey(FP, on_delete=models.CASCADE)
    ssid = models.CharField('ssid', max_length=32)
    mac = models.CharField('mac_address', max_length=17)
    rssi = models.SmallIntegerField('signal strength')
    freq = models.SmallIntegerField('frequency')
