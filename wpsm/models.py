from django.db import models
from datetime import datetime

# Create your models here.
class FP(models.Model):
    latitude = models.FloatField('latitude')
    longitude = models.FloatField('longitude')
    provider = models.CharField('provider', max_length=10)
    accuracy = models.FloatField('accuracy')

    user_lat = models.FloatField('user latitude', null=True)
    user_lng = models.FloatField('user longitude', null=True)

    app_name = models.CharField('app name that is gathering', max_length=50)
    position = models.CharField(max_length=30,null=True)
    reg_date = models.DateField('date published', default=datetime.today)


class ScanMac(models.Model):
    fp = models.ForeignKey(FP, on_delete=models.CASCADE)
    ssid = models.CharField('ssid', max_length=32)
    mac = models.CharField('mac_address', max_length=17)
    rssi = models.SmallIntegerField('signal strength')
    freq = models.SmallIntegerField('frequency')
