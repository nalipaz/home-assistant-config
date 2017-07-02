#!/usr/bin/env bash
mosquitto_pub -h home.alipaz.net -u plex -P "W@b5j7g9" -p 8883 --cafile ca.crt --key home.alipaz.net.key --cert home.alipaz.net.crt -i home-assistant-3 -t plex-watch/start -m "new"

{user} has started playing {title}