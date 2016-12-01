import os,yaml

def touch(fname, times=None):
    with open(fname, 'a'):
        os.utime(fname, times)

def arg_to_phone(argument):
    config = open('/home/plex/.homeassistant/.googlevoice', 'r')
    phones = yaml.load(config)

    return str(phones[argument])