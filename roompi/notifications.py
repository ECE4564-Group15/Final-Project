import pygame
import time
# from twilio.rest import TwilioRestClient
from gtts import gTTS
import os

'''this is for twilio'''
accountSID = "ACc8cb6ca47d0a8b36519bbd4180ab2a46"
authToken = "b58beb2a4fd808e24d3b38741f130f8c"

'''
' function: send_SMS()
' parameter: _SMS_ (the content of the msg)
' return: None
'''

#
# def send_SMS(_SMS_):
#     client = TwilioRestClient(accountSID, authToken)
#     client.messages.create(to="+15407509285", from_="+16173000913", body=_SMS_)
'''
' function: audio_notification
' parameter: sentence(content of the voice), filename(sound filename)
' return: None
'''

def audio_notification(sentence, filename):
    tts = gTTS(text=sentence, lang='en')
    tts.save(filename)
    play_music(filename)

'''
' function: play_music()
' parameter: None
' return: None
' Note: needs to configure continuous music playing
'       and music dir
'''

def play_music(filename):
    pygame.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    time.sleep(10)
'''
' function: init__LED()
' parameter: None
' return: none
' Note: change the pin number if needed.
'''

def init__LED():
    os.system("echo 17 > /sys/class/gpio/export || true") # blue
    os.system("echo 19 > /sys/class/gpio/export || true") # green
    os.system("echo 21 > /sys/class/gpio/export || true") # red
    os.system("echo out > /sys/class/gpio/gpio17/direction")
    os.system("echo out > /sys/class/gpio/gpio19/direction")
    os.system("echo out > /sys/class/gpio/gpio21/direction")

'''
' function: LED()
' parameter: color
' return: None
' Note: clear all light first and then turn corresponding on
'       change pin number if it is changed in the previous function
'''
def LED(color):
    os.system("echo 0 >/sys/class/gpio/gpio17/value")
    os.system("echo 0 >/sys/class/gpio/gpio19/value")
    os.system("echo 0 >/sys/class/gpio/gpio21/value")
    if(color == 'green'):
        os.system("echo 1 >/sys/class/gpio/gpio19/value")
    elif(color == 'blue'):
        os.system("echo 1 >/sys/class/gpio/gpio17/value")
    elif(color == 'red'):
        os.system("echo 1 >/sys/class/gpio/gpio21/value")
'''
' function: del_LED()
' parameter: None
' return: None
' Note: unregister the pins, so no error next time initialize the LED
'''
def del_LED():
    os.system("echo 17 > /sys/class/gpio/unexport || true") # blue
    os.system("echo 19 > /sys/class/gpio/unexport || true") # green
    os.system("echo 21 > /sys/class/gpio/unexport || true") # red