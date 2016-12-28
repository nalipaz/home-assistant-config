#!/usr/bin/env python3
## @file mqtt-locker.py
#  Utility script to lock/unlock computer based on waypoint region being entered.
#
#  The script Integrates with a screen locker by sending configurable lock and unlock command.
#
#  Configuration is stored in a separate `~/.proximity` file. An example of the file is provided in this repo under
#    `example-configs/.proximity`
#  @see example-configs/.proximity

from __future__ import print_function
import paho.mqtt.client as mqtt
import sys,os,yaml,getpass,time,subprocess,json

config_file = open('/home/' + getpass.getuser() + '/.proximity', 'r')
config = yaml.load(config_file)
timestamp = int(time.time())
topic = 'owntracks/{c[username]}/{c[tid]}/event'.format(c=config['credentials'])
# topic = 'owntracks/#'.format(c=config['credentials'])

def on_connect(client, userdata, rc):
    client.subscribe(topic, 2)

def on_message(client, userdata, msg):
    data = msg.payload.decode('utf-8')
    o = json.loads(data)
    event = o["event"]
    waypoint = o["desc"]

    if waypoint == config['zone']:
        if event == 'leave':
            # Put lock daemon starting into a separate command since it can error if daemon is already up for some lockers.
            os.system(config['commands']['lock_daemon'])
            # Lock the screen
            os.system(config['commands']['lock'])
        else:
            # Unlock the screen
            os.system(config['commands']['unlock'])
            # Wake up monitors
            os.system(config['commands']['wake_monitors'])

client = mqtt.Client()
client.username_pw_set(str(config['credentials']['username']), config['credentials']['password'])
client.tls_set(config['credentials']['certificate'])
client.on_connect = on_connect
client.on_message = on_message
client.connect(config['credentials']['host'], int(config['credentials']['port']), 60)

client.loop_forever()
