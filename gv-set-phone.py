#!/usr/bin/env python
from __future__ import print_function
from googlevoice import Voice,Phone,util
from gv-utils import arg_to_phone,touch
import sys

voice = Voice()
voice.login()

for phone in voice.phones:
    filename = '/home/plex/.homeassistant/states/' + str(sys.argv[2])
    touch(filename)
    if phone.phoneNumber == arg_to_phone(str(sys.argv[2])):
        if str(sys.argv[1]) == "enabled":
            phone.enable()
            with open(filename, "w") as f:
                f.write("enabled")
        elif str(sys.argv[1]) == "disabled":
            phone.disable()
            with open(filename, "w") as f:
                f.write("disabled")
