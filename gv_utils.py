import os,yaml,getpass

def touch(fname, times=None):
    with open(fname, 'a'):
        os.utime(fname, times)

def arg_to_phone(argument):
    config = open('/home/' + getpass.getuser() + '/.googlevoicephones', 'r')
    phones = yaml.load(config)

    return str(phones[argument])