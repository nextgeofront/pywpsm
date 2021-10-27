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
        print(filtered)
        df = pd.DataFrame(filtered)
        if df.empty:
            return JsonResponse({'fingerprint':-1, 'scan': macs, 'location': data['locations']})

        df_grp = df.groupby(['fp_id'])
        # print(df_grp.groups)
        sums = []
        wifi_towers = data['wifi_towers']
        for g in df_grp.groups:
            temp = df.loc[df['fp_id'] == g]
            sum = 0
            for w in wifi_towers:
                m = temp.loc[temp['mac'] == w['mac_address'].upper()]
                if not m.empty:
                    m_rssi = m['rssi'].values[0]
                    sum += abs(m_rssi - w['signal_strength'])
                else:
                    sum += abs(w['signal_strength'])
            sums.append([g, sum])
        df_min = pd.DataFrame(sums, columns=['fp_id', 'min'])
        print(df_min.to_dict('records'))
        fp = FP.objects.filter(id=df_min.loc[ df_min['min'] == df_min['min'].min()]['fp_id'].values[0])[0].__dict__
        print(fp)
    except Exception as ex:
        print(ex)
    return JsonResponse({'fingerprint':fp['id'],
                         'match': len_macs,
                         'location':[fp['user_lat'], fp['user_lng']],
                         'score': df_min.to_dict('records') })

