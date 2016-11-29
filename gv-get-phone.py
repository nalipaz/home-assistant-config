#!/usr/bin/env python
from googlevoice import Voice,Phone,util,Folder
from gv-phone-dict import arg_to_phone
import sys

voice = Voice()
voice.login()

execfile("/home/plex/.homeassistant/gv-phone-dict.py")

filename = '/home/plex/.homeassistant/states/' + str(sys.argv[2])

def returnValue():
    for phone in voice.phones:
        print phone.enabled()
        if phone.phoneNumber == arg_to_phone(str(sys.argv[1])):
            return 'enabled' if phone.enabled else 'disabled'

print returnValue()

