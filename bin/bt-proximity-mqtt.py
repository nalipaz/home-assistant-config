#!/usr/bin/env python3
## @file bt-proximity-mqtt.py
#  Utility script to send zone info to an owntracks mqtt server on bluetooth detection with blueproximity in Linux.
#
#  The script does a couple things.
#    1. When called it can send predefined zone information to an owntracks topic in an mqtt server.
#    2. As an added bonus it integrates with a screen locker by sending a lock and unlock command.0
#
#  Configuration is stored in a separate `~/.proximity` file. An example of the file is provided in this repo under
#    `example-configs/.proximity`
#  @see example-configs/.proximity

from __future__ import print_function
import paho.mqtt.client as mqtt
import sys,os,yaml,getpass,time,subprocess

config_file = open('/home/' + getpass.getuser() + '/.proximity', 'r')
config = yaml.load(config_file)
timestamp = int(time.time())
topic = 'owntracks/{c[username]}/{c[tid]}'.format(c=config['credentials'])

client = mqtt.Client()
client.username_pw_set(str(config['credentials']['username']), config['credentials']['password'])
client.tls_set(config['credentials']['certificate'])
client.connect(config['credentials']['host'], int(config['credentials']['port']), 60)

if len(sys.argv) > 1 and str(sys.argv[1]) == '-l':
    # Put lock daemon starting into a separate command since it can error if daemon is already up for some lockers.
    os.system(config['commands']['lock_daemon'])
    # Lock the screen
    os.system(config['commands']['lock'])
    # Send updated mqtt message about location to hass
    data = '{{"_type":"transition","wtst":{t},"tst":{t},"lat":{m[latitude]},"lon":{m[longitude]},"acc":2,"tid":"{c[tid]}","event":"leave","desc":"{m[zone]}","t":"c"}}'.format(c=config['credentials'], m=config['away_message'], t=timestamp)
    client.publish(topic, data)
    data = '{{"_type":"location","tid":"{c[tid]}","acc":27,"conn":"w","doze":false,"lat":{m[latitude]},"lon":{m[longitude]},"tst":{t},"event":"leave","desc":"{m[zone]}","t":"c"}}'.format(c=config['credentials'], m=config['away_message'], t=timestamp)
    client.publish(topic, data)
else:
    if len(sys.argv) > 1 and str(sys.argv[1]) == '-u':
        # Unlock the screen
        os.system(config['commands']['unlock'])
        # Wake up monitors
        os.system(config['commands']['wake_monitors'])
    data = '{{"_type":"transition","wtst":{t},"tst":{t},"lat":{m[latitude]},"lon":{m[longitude]},"acc":2,"tid":"{c[tid]}","event":"enter","desc":"{m[zone]}","t":"c"}}'.format(c=config['credentials'], m=config['message'], t=timestamp)
    client.publish(topic, data)
    data = '{{"_type":"location","tid":"{c[tid]}","acc":27,"conn":"w","doze":false,"lat":{m[latitude]},"lon":{m[longitude]},"tst":{t},"event":"enter","desc":"{m[zone]}","t":"c"}}'.format(c=config['credentials'], m=config['message'], t=timestamp)
    client.publish(topic, data)

client.disconnect()
