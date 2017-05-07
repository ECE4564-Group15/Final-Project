#!/usr/bin/env python3

from __future__ import print_function
import RPi.GPIO as GPIO
import MFRC522
import signal
import time
import UserClient
import pickle

import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

continue_reading = True


try:
    import argparse
    parser = argparse.ArgumentParser(parents=[tools.argparser])
    parser.add_argument('--server',help='Enter the database IP address')
    flags = parser.parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Steven Quick'

def get_credentials():
    credential_path = os.path.join('',
                                   'temp.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def print_information(ID, color):
    print()
    print('Your personal ID is set to ', ID)
    print('The prefered LED color is set to be ',color)
    print('Transmit to database...Done')
    print()
    
def sign_up(uid, c):
    credentials = get_credentials()
    pickle_cred = pickle.dumps(credentials)
    
    os.remove('temp.json')
    ID = '.'.join(str(x) for x in uid)
    #integrate this part to a web interface

    print()
    finished = False
    color = None

    print('We provide LED notification color in red or green')
    while (finished == False):
        color = input('Choose your favorite one: ')
        if (color == 'red' or color == 'green'):
            finished = True
        else:
            print('Sorry, we currently do not provide ', color , 'as LED light color.')
    
    print_information(ID, color)
    
    #then post personal information to database
    if (c.new_user(ID,color,pickle_cred) == False):
        c.update_user(ID,color,pickle_cred)
    

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

GPIO.setup(15,GPIO.OUT)
print('Please Tap your RFID to our reader')

server = flags.server
if (server == None):
    c = UserClient.UserClient('localhost')
else:
    c = UserClient.UserClient(flags.server)
c.connect()

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    if status == MIFAREReader.MI_OK:
        print("Card detected")
        #credential = get_credentials()
        
    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:
        print("UID: %s,%s,%s,%s" % (uid[0],uid[1],uid[2],uid[2]))
        sign_up(uid, c)

