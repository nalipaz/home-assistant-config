#!/usr/bin/env python
from googlevoice import Voice,Phone,util,Folder
import sys

voice = Voice()
voice.login()

#util.pprint(voice.settings)
#util.pprint(voice.contacts['phones'].values())

execfile("/home/plex/.homeassistant/gv-phone-dict.py")

def returnValue():
    for phone in voice.phones:
        print phone.enabled()
        if phone.phoneNumber == arg_to_phone(str(sys.argv[1])):
            return 'enabled' if phone.enabled else 'disabled'

print returnValue()

