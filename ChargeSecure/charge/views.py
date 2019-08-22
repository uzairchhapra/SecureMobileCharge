from django.shortcuts import render
from django.http import HttpResponse
from .models import *
import json

def index(request):
    return render(request, 'charge/index.html')

def maps(request):
    print('hello')
    return render(request, 'charge/maps2.html')

def getlocation(request):
    result_set = ChargeStation.objects.all().values()
    t = []
    for i in result_set:
        t.append(i)
        print(t)
    return HttpResponse(json.dumps(t), content_type='application/json')

# Create your views here.
