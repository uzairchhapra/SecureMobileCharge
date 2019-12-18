from django.shortcuts import render
from django.http import HttpResponse
from .models import *
import json
from django.urls import reverse #coverts name to url

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
<<<<<<< HEAD

host = 'a1wlltnsvntckz-ats.iot.ap-south-1.amazonaws.com'
rootCAPath = '/Users/adityachavan/Documents/GitHub/SecureMobileCharge/ChargeSecure/charge/certificates/server/root-CA.pem'
certificatePath = '/Users/adityachavan/Documents/GitHub/SecureMobileCharge/ChargeSecure/charge/certificates/server/45447d2f06-certificate.pem.crt'
privateKeyPath = '/Users/adityachavan/Documents/GitHub/SecureMobileCharge/ChargeSecure/charge/certificates/server/45447d2f06-private.pem.key'
=======
    print("Received a new message: ")
    print(message.payload)


host = 'a1wlltnsvntckz-ats.iot.ap-south-1.amazonaws.com'
rootCAPath = 'charge/certificates/server/root-CA.pem'
certificatePath = 'charge/certificates/server/45447d2f06-certificate.pem.crt'
privateKeyPath = 'charge/certificates/server/45447d2f06-private.pem.key'
>>>>>>> b24f8cac40019fb7bd73ef677f8f922aefebd02e
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
<<<<<<< HEAD
if useWebsocket:
    myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId, useWebsocket=True)
    myAWSIoTMQTTClient.configureEndpoint(host, port)
    myAWSIoTMQTTClient.configureCredentials(rootCAPath)
else:
    myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
    myAWSIoTMQTTClient.configureEndpoint(host, port)
    myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

=======

myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
myAWSIoTMQTTClient.configureEndpoint(host, port)
myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)
    
>>>>>>> b24f8cac40019fb7bd73ef677f8f922aefebd02e
# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 1, 2)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(5)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

myAWSIoTMQTTClient.connect()

myAWSIoTMQTTClient.subscribe(topic, 1, customCallback)

# def authenticate(request):
#     username = request.POST['username']
#     password = request.POST['password']
#     l = Student.objects.filter(username=username, password=password)
#     if len(l):
#         request.session['username'] = username
#         return HttpResponseRedirect(reverse('index'))
#     else:
#         return HttpResponseRedirect(reverse('index'))

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

<<<<<<< HEAD
def book_a_locker(request):

=======
def get_free_slots(request, station_number):
    free_slots = []
    for i in Slot.objects.filter(cid=station_number):#get all slots in station
        if i.status == 'unused':
            free_slots.append(i)
    return free_slots


def book_slot(request, station_number, phone_status, action):

    slot = Book.objects.filter(uid = request.user).order_by('-action_time') #current slot of user
    if (action == 'close' or phone_status == 'inside') and (len(slot) == 0 or slot[0].sid.status == 'unused')  :
        return ["Error","First put your Phone inside"]
    elif action == 'close' or phone_status == 'inside':
        slot = slot[0].sid

    if action == 'open':
        if phone_status == 'outside':
            if len(slot) != 0 and slot[0].sid.status == 'used':
                return ["Error","Your Phone is already inside"]
            # If phone is outside the charging slot
            # Checking if slots available in station
            slot = get_free_slots(request,station_number)
            if len(slot)>0: # if slots are available
                slot = slot[0]
                Book.objects.create(uid = request.user, sid = slot, phone_status = 'outside', action = 'open').save() #new slot alloted to user
                slot.status = 'used'
                slot.save()
            else:
                return []
        elif phone_status == 'inside': # open slot after charging
            Book.objects.create(uid = request.user, sid = slot, phone_status = 'inside', action = 'open').save()
    
    elif action == 'close':
        if phone_status == 'outside':
            Book.objects.create(uid = request.user, sid = slot, phone_status = 'outside', action = 'close').save()
            slot.status = 'unused'
            slot.save()
        elif phone_status == 'inside':
            Book.objects.create(uid = request.user, sid = slot, phone_status = 'inside', action = 'close').save()
    return [slot]

def publish_to_station(request):
    #Getting station action details
    station_number = request.GET['station']
    action = request.GET['action']
    phone_status = request.GET['phone_status']
    topic = 'dev'+str(station_number)

    slot = book_slot(request, station_number, phone_status, action)

    message = {}
    message['phone_status'] = phone_status
    message['message'] = 'from_server'
    message['error'] = False

    if len(slot) == 0 :
        #Slots Unavailable
        message['error'] = True
        message['error_desc'] = "Slots Unavailable"
        messageJson = json.dumps(message)
        # return HttpResponse(messageJson)
    elif len(slot) == 2 :
        #Slots Unavailable
        message['error'] = True
        message['error_desc'] = slot[1]
        messageJson = json.dumps(message)
        # return HttpResponse(messageJson)
    else:
        #Slot Available
        message['slot'] = slot[0].slot_number
        message['station_number'] = station_number
        message['action'] = action
        # message['phone_status'] = phone_status
        messageJson = json.dumps(message)

    publish_status = myAWSIoTMQTTClient.publish(topic, messageJson, 1)

    if publish_status == True:
        #Published Successfully
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
>>>>>>> b24f8cac40019fb7bd73ef677f8f922aefebd02e
    message = {}
    message['message'] = mess
    message['sequence'] = loopcount
    messageJson = json.dumps(message)
<<<<<<< HEAD
    myAWSIoTMQTTClient.publish(topic, messageJson, 1)
    return HttpResponse('Published topic %s: %s\n' % (topic, messageJson))
=======
    wow = myAWSIoTMQTTClient.publish(topic, messageJson, 1)
    print('Published topic %s: %s\n' % (topic, messageJson))

    return HttpResponse('Published topic %s: %s\n%s' % (topic, messageJson,str(wow)))
>>>>>>> b24f8cac40019fb7bd73ef677f8f922aefebd02e
