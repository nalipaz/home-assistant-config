# Home Assistant Configuration

My personal home-assistant config files.

## Devices

 * ODroid XU4 (1)
     * Server, runs Debian Jessie compiled using Armbian.
 * Aeotech Z-Stick Gen5
     * Main Z-Wave controller connected to server
 * GE In-Wall On/Off Switch (1)
     * Front porch light switch
 * GE In-Wall Dimmer Switch (1)
     * Living room light switch
 * GE In-Wall Outlets (3)
     * Front Porch outlet (Front Window Christmas lights)
     * Dining room outlet (Christmas tree)
 * Chamberlain Garage door opener - myQ enabled (1)
     * Controls garage door
 * [Irdroid USB Transceiver](http://www.irdroid.com/irdroid-usb-ir-transceiver/) (1)
     * Living room TV remote
     * Bluray player remote
     * iClebo vacuum remote (only when in range of IR transceiver of course)
 * Android Phone
     * Used in conjunction with Owntracks to notify of arrivals and departures from home/work.
 * Google Home (1)

## Software-based Integrations

 * Google Voice
     * [pygooglevoice](https://github.com/pettazz/pygooglevoice) integrated with a few python scripts I wrote I am able to toggle the Google Voice call forwarding state on the phones in my account.
 * Mosquitto server
     * Server has mosquitto running for communication with Owntracks on phone.
 * Plex server
     * Plex monitoring and control via the plex media player component

## Services

The server has many services running. These are the main ones:

 * Home Assistant (of course)
 * Plex media server
 * HTPC Manager
 * Mosquitto
 * NZBGet
 * Pi-Hole
 * Plexpy
 * Sonarr
 * Radarr
 * Headphones
 * Jackett
 * Lirc

Most of these services are monitored via home-assistant and can be quickly restarted from a hass switch if needed.

## Servers
Home assistant is also setup to monitor a few servers in the house. The monitoring is a simple ping to be sure they are up, when they go down I receive notifications.

 * Obihai OBi200 - For voip with Google voice
 * Plex Client - A client running in our guest room. It runs on a raspberry pi using rasplex.
 * Canon Printer - This is a wifi printer and it is monitored to see that it stays on the network as well as ink levels using a custom component.
