#!/usr/bin/env python
from __future__ import print_function
from googlevoice import Voice,Phone,util
import sys,os,yaml,getpass

def touch(fname, times=None):
    with open(fname, 'a'):
        os.utime(fname, times)

def arg_to_phone(argument):
    config = open('/home/' + getpass.getuser() + '/.googlevoicephones', 'r')
    phones = yaml.load(config)

    return str(phones[argument])

voice = Voice()
voice.login()

for phone in voice.phones:
    filename = '/home/' + getpass.getuser() + '/.googlevoicephonestates/' + str(sys.argv[2])
    touch(filename)
    if phone.phoneNumber == arg_to_phone(str(sys.argv[2])):
        getattr(phone, sys.argv[1])()
