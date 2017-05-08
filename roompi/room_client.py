from __future__ import print_function
"""
ECE 4564 Network Application Design: Final Project
Filename: room_client.py
Author: Xianze Meng
Last Modified: 5/7/2017

This script provides the functions needed by the room_client
"""
import time
import os
import UserClient
import sys
import threading
import MFRC522
import signal
import httplib2
from apiclient import discovery
from oauth2client import tools
import RPi.GPIO as GPIO
import datetime
import pickle
import logging
# from notifications import *
from gtts import gTTS

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_id.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'
logging.basicConfig(filename='event.log', format='%(asctime)s %(message)s', level=logging.INFO)

def audio_notification(sentence, filename):
    tts = gTTS(text=sentence, lang='en')
    tts.save(filename)
    play_music(filename)

def play_music(filename):
   os.system("omxplayer %s" % filename) 
   time.sleep(10)


def getEvents(credentials):
    """
    Retrieves events from the user's calendar
    :param credentials: User account's credential
    :return: A list of the next 10 events or None
    """
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    eventsResult = service.events().list(
        calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])
    return events

def flashRedLED():
    GPIO.output(15, GPIO.HIGH)
    time.sleep(0.75)
    GPIO.output(15, GPIO.LOW)
    time.sleep(0.75)

def flashGreenLED():
    GPIO.output(13, GPIO.HIGH)
    time.sleep(0.75)
    GPIO.output(13, GPIO.LOW)
    time.sleep(0.75)


def flashLEDs():
    flashRedLED()
    flashGreenLED()




# Tracks Client Using Dictionary
clients = {}

# Logging events
logging.basicConfig(filename='event.log', format='%(asctime)s %(message)s', level=logging.INFO)

# Sever Connection Object
server = UserClient.UserClient(sys.argv[1])
server.connect()

# Install signal handler--------------------------------------------------
def exitclean():
    l = clients.keys()
    for k in l:
        del clients[k]
    print("clean up!")
    time.sleep(1)
    GPIO.cleanup()
    quit()

signal.signal(signal.SIGINT, exitclean)
signal.signal(signal.SIGTSTP, exitclean)
# --------------------------------------------------------------------------

MIFAREReader = MFRC522.MFRC522()
GPIO.setup(15, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)

def clienthandler(uid):
    userinfo = server.get_user_info(uid)
    if userinfo is None:
        flashRedLED()
        audio_notification('Please register first', 'please_register.mp3')
        logging.info('{} tries to log in but has not registered yet'.format(uid))
        return
    # print('User Info: ', userinfo)
    logging.info('{} has logged in'.format(uid))
    try:
        user_credentials = pickle.loads(userinfo['credentials'])
    except KeyError:
        print("Key error while getting user credentials")
        GPIO.cleanup()
        exit()
    except Exception as e:
        print(type(e))
        print("Error while getting user credentials")
        GPIO.cleanup()
        exit()



    events = getEvents(user_credentials)
    while uid in clients:
        if events:
            logging.info("{}'s event has been collected".format(uid))
            for i in range(len(events)):
                e = datetime.datetime.strptime(events[i]['start'].get('dateTime', events[i]['start'].get('date'))[:-6], '%Y-%m-%dT%H:%M:%S')
                events[i] = (e, events[i]['summary'])
            now = datetime.datetime.now()
            for item in events:
                if now.minute - item.minute > 0:
                    events.remove(item)

            if (now+datetime.timedelta(minutes=5)) >= events[0][0]:
                t = events[0][0].minute - now.minute
                audio_notification("Attention, you have an event about {} in {} minutes".format(events[0][1], t), uid)
                logging.info("Notify {} event in 5 min".format(uid))
                while datetime.datetime.now() < (now + datetime.timedelta(seconds=15)):
                    flashLEDs()
            elif (now+datetime.timedelta(minutes=15)) >= events[0][0]:
                t = events[0][0].minute - now.minute
                logging.info("Notify {} event in {} min".format(uid, t))
                audio_notification("Attention, you have an event about {} in {} minutes".format(events[0][1], t), uid)
                while datetime.datetime.now() < (now + datetime.timedelta(seconds=15)):
                    flashLEDs()                    
        
        time.sleep(120)
        events = getEvents(user_credentials)
        logging.info("Updating {}'s event list".format(uid))

    logging.info("User {} has logged out".format(uid))
    return

while True:

    # Scan for cards
    (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)


    # Get the UID of the card
    (status, ruid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:

        uid = '.'.join(str(v) for v in ruid).strip()
        if uid not in clients:
            clients[uid] = threading.Thread(name=uid, target=clienthandler, args=(uid, ))
            clients[uid].run()
        else:
            del clients[uid]

        time.sleep(1)



