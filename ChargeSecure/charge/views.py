from django.shortcuts import render
from django.http import HttpResponse
from .models import *
import json


#AWS imports
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import argparse


def customCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")

host = 'a1wlltnsvntckz-ats.iot.ap-south-1.amazonaws.com'
rootCAPath = '/Users/adityachavan/Documents/GitHub/SecureMobileCharge/ChargeSecure/charge/certificates/server/root-CA.pem'
certificatePath = '/Users/adityachavan/Documents/GitHub/SecureMobileCharge/ChargeSecure/charge/certificates/server/45447d2f06-certificate.pem.crt'
privateKeyPath = '/Users/adityachavan/Documents/GitHub/SecureMobileCharge/ChargeSecure/charge/certificates/server/45447d2f06-private.pem.key'
port = 8883 # When no port override for non-WebSocket, default to 8883
#port = 443 # When no port override for WebSocket, default to 443

useWebsocket = False
clientId = 'server'
topic = 'pub'
mess='UzC'
mode='publish'

# Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = None
if useWebsocket:
    myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId, useWebsocket=True)
    myAWSIoTMQTTClient.configureEndpoint(host, port)
    myAWSIoTMQTTClient.configureCredentials(rootCAPath)
else:
    myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
    myAWSIoTMQTTClient.configureEndpoint(host, port)
    myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTClient connection configuration
# myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT
myAWSIoTMQTTClient.connect()




# ---------------------------------------------
# ____________________________________________
# ----------------------------------------------
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

def book_a_locker(request):

    message = {}
    message['message'] = mess
    message['sequence'] = 1
    messageJson = json.dumps(message)
    myAWSIoTMQTTClient.publish(topic, messageJson, 1)
    return HttpResponse('Published topic %s: %s\n' % (topic, messageJson))
