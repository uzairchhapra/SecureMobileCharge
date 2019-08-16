from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'charge/index.html')

def maps(request):
    print('hello')
    return render(request, 'charge/maps2.html')

# Create your views here.
