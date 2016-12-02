#!/usr/bin/env python
from __future__ import print_function
from googlevoice import Voice,Phone,util,Folder
from gv_utils import arg_to_phone
import sys,getpass

voice = Voice()
voice.login()

filename = '/home/' + getpass.getuser() + '/.googlevoicephonestates/' + str(sys.argv[1])

def returnValue():
    for phone in voice.phones:
        with open(filename, "r") as f:
            if phone.phoneNumber == arg_to_phone(str(sys.argv[1])):
                print(f.read())

returnValue()
