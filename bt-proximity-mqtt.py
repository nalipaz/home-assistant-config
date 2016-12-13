#!/usr/bin/env python3
from __future__ import print_function
import paho.mqtt.client as mqtt
import sys,os,yaml,getpass,time

config_file = open('/home/' + getpass.getuser() + '/.proximity', 'r')
config = yaml.load(config_file)
timestamp = int(time.time())
topic = 'owntracks/{c[username]}/{c[tid]}'.format(c=config['credentials'])

client = mqtt.Client()
client.username_pw_set(str(config['credentials']['username']), config['credentials']['password'])
client.tls_set(config['credentials']['certificate'])
client.connect(config['credentials']['host'], int(config['credentials']['port']), 60)

if len(sys.argv) > 1 and str(sys.argv[1]) == 'lock':
    data = '{{"_type":"transition","wtst":{t},"tst":{t},"lat":{m[latitude]},"lon":{m[longitude]},"acc":2,"tid":"{c[tid]}","event":"leave","desc":"{m[zone]}","t":"c"}}'.format(c=config['credentials'], m=config['away_message'], t=timestamp)
    client.publish(topic, data)
    data = '{{"_type":"location","tid":"{c[tid]}","acc":27,"conn":"w","doze":false,"lat":{m[latitude]},"lon":{m[longitude]},"tst":{t},"event":"leave","desc":"{m[zone]}","t":"c"}}'.format(c=config['credentials'], m=config['away_message'], t=timestamp)
    client.publish(topic, data)
else:
    data = '{{"_type":"transition","wtst":{t},"tst":{t},"lat":{m[latitude]},"lon":{m[longitude]},"acc":2,"tid":"{c[tid]}","event":"enter","desc":"{m[zone]}","t":"c"}}'.format(c=config['credentials'], m=config['message'], t=timestamp)
    client.publish(topic, data)
    data = '{{"_type":"location","tid":"{c[tid]}","acc":27,"conn":"w","doze":false,"lat":{m[latitude]},"lon":{m[longitude]},"tst":{t},"event":"enter","desc":"{m[zone]}","t":"c"}}'.format(c=config['credentials'], m=config['message'], t=timestamp)
    client.publish(topic, data)

client.disconnect()
