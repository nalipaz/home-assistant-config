import homeassistant.loader as loader
import sys,os

# The domain of your component. Should be equal to the name of your component.
DOMAIN = "plex_title_mqtt"

# List of component names (string) your component depends upon.
DEPENDENCIES = ['mqtt']


CONF_TOPIC = 'topic'
DEFAULT_TOPIC = 'plex/title'


def setup(hass, config):
    mqtt = loader.get_component('mqtt')
    topic = config[DOMAIN].get('topic', DEFAULT_TOPIC)
    entity_id = 'plex_title_mqtt.last_message'

    # Listener to be called when we receive a message.
    def message_received(topic, payload, qos):
        """A new MQTT message has been received."""
        hass.states.set(entity_id, payload)

    # Subscribe our listener to a topic.
    mqtt.subscribe(hass, topic, message_received)

    # Set the intial state
    hass.states.set(entity_id, 'No messages')

    # Service to publish a message on MQTT.
    def set_state_service(call):
        """Service to send a message."""
        # print repr("curl -s http://127.0.0.1:32400/library/metadata/" +  str(hass.states.get('media_player.tv_un55h6300.attributes.media_content_id')) + "?X-Plex-Token=" + str(hass.states.get('sensor.plex_token')) + " | xmlstarlet sel -t -v '//Video/@grandparentTitle' | mosquitto_pub -t plex/title -s")
        mqtt.publish(hass, topic, os.popen("curl -s http://127.0.0.1:32400/library/metadata/" +  str(hass.states.get('media_player.tv_un55h6300.attributes.media_content_id')) + "?X-Plex-Token=" + str(hass.states.get('sensor.plex_token')) + " | xmlstarlet sel -t -v '//Video/@grandparentTitle' | mosquitto_pub -t plex/title -s").read())

    # Register our service with Home Assistant.
    hass.services.register(DOMAIN, 'set_state', set_state_service)

    # Return boolean to indicate that initialization was successfully.
    return True