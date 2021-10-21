from django.shortcuts import render
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.
@csrf_exempt
def insert_fp(request):
    data = json.loads(request.body)
    return JsonResponse(data=data)