from django.shortcuts import render
from django.http import HttpResponse
from .models import *
import json


#AWS imports
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import argparse

loopcount=0
y=0
li=[]

def customCallback(client, userdata, message):
    global y
    y+=1
    li.append((y,message.payload))
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")
    print("Received a new message: ")
    print(message.payload)

'''  #remove when connected to internet

host = 'a1wlltnsvntckz-ats.iot.ap-south-1.amazonaws.com'
rootCAPath = 'charge/certificates/server/root-CA.pem'
certificatePath = 'charge/certificates/server/45447d2f06-certificate.pem.crt'
privateKeyPath = 'charge/certificates/server/45447d2f06-private.pem.key'
port = 8883 # When no port override for non-WebSocket, default to 8883
#port = 443 # When no port override for WebSocket, default to 443

useWebsocket = False
clientId = 'server'
topic = 'server'

# Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = None

myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
myAWSIoTMQTTClient.configureEndpoint(host, port)
myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)
    
# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 1, 2)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(5)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

myAWSIoTMQTTClient.connect()

myAWSIoTMQTTClient.subscribe(topic, 1, customCallback)
'''

def is_subscribed(request):
    return HttpResponse(str(li))

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

def get_free_slot(station_number):
    return 3

def publish_to_station(request):
    #Getting station action details
    station_number = request.GET['station']
    action = request.GET['action']
    topic = station_number

    #Checking if slots available in station
    slot = get_free_slot(station_number)

    message = {}
    message['message'] = 'from_server'
    message['slot'] = slot
    message['error'] = False

    if slot == -1:
        #Slots Unavailable
        message['error'] = True
        message['error_desc'] = "Slots Unavailable"
        messageJson = json.dumps(message)
        return HttpResponse(messageJson)
    else:
        #Slot Available
        message['station_number'] = station_number
        message['action'] = action
#remove when connected to internet        # publish_status = myAWSIoTMQTTClient.publish(topic, messageJson, 1)
        publish_status = True
        if publish_status == True:
            #Published Successfully
            messageJson = json.dumps(message)
            print('Published topic %s: %s\n' % (topic, messageJson))
            return HttpResponse('Published topic %s: %s' % (topic, messageJson))
        else:
            #Published Unsuccessfully
            message['error'] = True
            message['error_desc'] = 'Failed to reach Server'
            messageJson = json.dumps(message)
            return HttpResponse('Published topic %s: %s' % (topic, messageJson))

def book_a_locker(request):
    global loopcount

    if loopcount%2==0:
        topic = 'dev1'
    else :
        topic = 'dev2'
    mess='from_server'

    loopcount+=1
    message = {}
    message['message'] = mess
    message['sequence'] = loopcount
    messageJson = json.dumps(message)
    wow = myAWSIoTMQTTClient.publish(topic, messageJson, 1)
    print('Published topic %s: %s\n' % (topic, messageJson))

    return HttpResponse('Published topic %s: %s\n%s' % (topic, messageJson,str(wow)))