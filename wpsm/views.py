from django.shortcuts import render
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import FP, ScanMac
import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn import preprocessing
from sklearn.preprocessing import OneHotEncoder

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
        macs = [w['mac_address'].upper() for w in data['wifi_towers'] if w['signal_strength'] >= -85]
        len_macs = len(macs)
        filtered = ScanMac.objects.filter(mac__in=macs).values()
        df = pd.DataFrame(filtered)
        le = preprocessing.LabelEncoder()
        df['mac_le'] = le.fit_transform(df['mac'])
        # df = df.set_index(['mac_le', 'rssi']).reset_index()
        df_grp = df.groupby(['mac_le'])
        for g in df_grp.groups:
            print(df.loc[df['mac_le'] == g])

        # df_grp['percentage'] = df_grp['counts']/len_macs
        # b = df_grp.loc[df_grp['percentage']]
        # print(b)
        # c = FP.objects.filter(id__in=list(b['fp_id']))
        # print(c)


    except Exception as ex:
        print(ex)
    return JsonResponse({'result':0})

