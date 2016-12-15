#!/usr/bin/env python
## @file gv-phone.py
#  Utility script to set google voice call forwarding using pygooglevoice library.
#
#  Configuration is stored in a separate `~/.googlevoicephones` file. An example of the file is provided in this repo under
#    `example-configs/.googlevoicephones`
from __future__ import print_function
from googlevoice import Voice,Phone,util
import sys,os,yaml,getpass

## Utility function to return a proper phone number/email address based on a named alias.
#
#  This allows us to keep phone numbers out of code and only accessible from the config file via a named alias.
#
#  @see example-configs/.googlevoicephones
#
#  @param string argument The named phone alias to lookup the number in the config file.
def arg_to_phone(argument):
    config = open('/home/' + getpass.getuser() + '/.googlevoicephones', 'r')
    phones = yaml.load(config)

    return str(phones[argument])

voice = Voice()
voice.login()

for phone in voice.phones:
    if phone.phoneNumber == arg_to_phone(str(sys.argv[2])):
        getattr(phone, sys.argv[1])()
