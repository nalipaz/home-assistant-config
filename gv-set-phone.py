#!/usr/bin/env python
from googlevoice import Voice,Phone,util
import sys

voice = Voice()
voice.login()

execfile("/home/plex/.homeassistant/gv-phone-dict.py")

for phone in voice.phones:
    if phone.phoneNumber == arg_to_phone(str(sys.argv[2])):
        if str(sys.argv[1]) == "enabled":
            phone.enable()
        elif str(sys.argv[1]) == "disabled":
            phone.disable()

