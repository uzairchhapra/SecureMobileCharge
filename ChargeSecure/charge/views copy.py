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


host = 'a1wlltnsvntckz-ats.iot.ap-south-1.amazonaws.com'
rootCAPath = 'C:/Users/Sameer/Documents/GitHub/SecureMobileCharge/ChargeSecure/charge/certificates/server/root-CA.pem'
certificatePath = 'C:/Users/Sameer/Documents/GitHub/SecureMobileCharge/ChargeSecure/charge/certificates/server/45447d2f06-certificate.pem.crt'
privateKeyPath = 'C:/Users/Sameer/Documents/GitHub/SecureMobileCharge/ChargeSecure/charge/certificates/server/45447d2f06-private.pem.key'
port = 8883 # When no port override for non-WebSocket, default to 8883
#port = 443 # When no port override for WebSocket, default to 443

useWebsocket = False
clientId = 'server'
topic = 'pub'
mess='from_server'

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

def book_a_locker(request):
    global loopcount
    host = 'a1wlltnsvntckz-ats.iot.ap-south-1.amazonaws.com'
    rootCAPath1 = 'C:/Users/Sameer/Documents/GitHub/SecureMobileCharge/ChargeSecure/charge/certificates/dev1/root-CA.pem'
    certificatePath1 = 'C:/Users/Sameer/Documents/GitHub/SecureMobileCharge/ChargeSecure/charge/certificates/dev1/1e5e1bc664-certificate.pem.crt'
    privateKeyPath1 = 'C:/Users/Sameer/Documents/GitHub/SecureMobileCharge/ChargeSecure/charge/certificates/dev1/1e5e1bc664-private.pem.key'
    port = 8883 # When no port override for non-WebSocket, default to 8883
    #port = 443 # When no port override for WebSocket, default to 443

    clientId1 = 'chargebuddy'
    topic = 'pub'
    mess='from_server'

    # Configure logging
    logger1 = logging.getLogger("AWSIoTPythonSDK.core")
    logger1.setLevel(logging.DEBUG)
    streamHandler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    streamHandler.setFormatter(formatter)
    logger1.addHandler(streamHandler)

    # Init AWSIoTMQTTClient
    myAWSIoTMQTTClient1 = None
    
    myAWSIoTMQTTClient1 = AWSIoTMQTTClient(clientId1)
    myAWSIoTMQTTClient1.configureEndpoint(host, port)
    myAWSIoTMQTTClient1.configureCredentials(rootCAPath1, privateKeyPath1, certificatePath1)
    
    # AWSIoTMQTTClient connection configuration
    myAWSIoTMQTTClient1.configureAutoReconnectBackoffTime(1, 1, 2)
    myAWSIoTMQTTClient1.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
    myAWSIoTMQTTClient1.configureDrainingFrequency(5)  # Draining: 2 Hz
    myAWSIoTMQTTClient1.configureConnectDisconnectTimeout(10)  # 10 sec
    myAWSIoTMQTTClient1.configureMQTTOperationTimeout(5)  # 5 sec


    # Connect and subscribe to AWS IoT
    myAWSIoTMQTTClient1.connect()
    loopcount+=1
    message = {}
    message['message'] = mess
    message['sequence'] = loopcount
    messageJson = json.dumps(message)
    wow = myAWSIoTMQTTClient1.publish(topic, messageJson, 1)
    myAWSIoTMQTTClient1.disconnect()

    return HttpResponse('Published topic %s: %s\n%s' % (topic, messageJson,str(wow)))