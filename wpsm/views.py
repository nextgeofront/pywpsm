from django.shortcuts import render
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import FP, ScanMac

# Create your views here.
@csrf_exempt
def insert_fp(request):
    data = json.loads(request.body)
    try:
        fp = FP.objects.create(latitude=data['locations']['latitude'],
           longitude=data['locations']['longitude'],
           provider=data['locations']['provider'],
           accuracy=data['locations']['accuracy'],
           user_lat=data['device_info']['latitude'],
           user_lng=data['device_info']['longitude'],
           app_name=data['device_info']['package_name'],
           position=data['device_info']['position'])
        scan_macs = []
        for scan in data['wifi_towers']:
            scan_macs.append(ScanMac(fp_id=fp,
                                     ssid=scan['ssid'],
                                     mac=scan['mac_address'].upper(),
                                     rssi=scan['signal_strength'],
                                     freq=scan['frequency']))
        ScanMac.objects.bulk_create(scan_macs)
    except Exception as ex:
        print(ex)
    return JsonResponse(data=data)

@csrf_exempt
def wps(request):
    data = json.loads(request.body)
    return JsonResponse({})

