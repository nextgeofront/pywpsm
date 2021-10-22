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
        fp = FP.objects.create(
            latitude=data['locations']['latitude'],
           longitude=data['locations']['longitude'],
           provider=data['locations']['provider'],
           accuracy=data['locations']['accuracy'],
           user_lat=data['pin']['pin_latitude'],
           user_lng=data['pin']['pin_longitude'],
           position=data['pin']['bld_name'],
           package_name=data['package_name']
                               )
        scan_macs = []
        for scan in data['wifi_towers']:
            scan_macs.append(ScanMac(fp_id=fp.id,
                                     ssid=scan['ssid'],
                                     mac=scan['mac_address'].upper(),
                                     rssi=scan['signal_strength'],
                                     freq=scan['frequency']))
        ScanMac.objects.bulk_create(scan_macs)
    except Exception as ex:
        print(ex)
        return JsonResponse({'result':-1})
    return JsonResponse({'result':0})

@csrf_exempt
def wps(request):
    data = json.loads(request.body)
    try:
        wifi_towers = data['wifi_towers']
        macs = [w['mac_address'].upper() for w in wifi_towers if w['signal_strength'] >= -85]
        print(len(macs), macs)
        filtered = ScanMac.objects.filter(mac__in=macs)

        print([f.fp_id for f in filtered])

    except Exception as ex:
        print(ex)
    return JsonResponse({'result':0})

