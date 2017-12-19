"""
Support for retrieving ink levels from supported printers.
Only works when ink is install in linux host.

configuration.yaml

sensor:
  - platform: ink
    host: IP_ADDRESS
    scan_interval: 120
    colors:
     - not_present
     - black
     - color
     - photo
     - cyan
     - magenta
     - yellow
     - photoblack
     - photocyan
     - photomagenta
     - photoyellow
     - red
     - green
     - blue
     - light_black
     - light_cyan
     - light_magenta
     - light_light_black
     - matte_black
     - gloss_optimizer
     - unknown
     - light_cyan_light_magenta_photoblack
     - 2x_grey_and_black
     - black_cyan_magenta_yellow
     - photocyan_and_photomagenta
     - yellow_and_magenta
     - cyan_and_black
     - light_grey_and_photoblack
     - light_grey
     - medium_grey
     - photogrey
     - white
"""
import logging
from datetime import timedelta
import requests
import voluptuous as vol
import subprocess
from subprocess import Popen, PIPE

from homeassistant.components.sensor import PLATFORM_SCHEMA
import homeassistant.helpers.config_validation as cv
from homeassistant.const import (
    CONF_HOST, CONF_SCAN_INTERVAL, CONF_RESOURCES)
from homeassistant.util import Throttle
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=120)

SENSOR_PREFIX = 'Ink '

SENSOR_TYPES = {
    'not_present': ['Not Present', '', 'mdi:flash'],
    'black': ['Black', '', 'mdi:flash'],
    'color': ['Color', '', 'mdi:flash'],
    'photo': ['Photo', '', 'mdi:flash'],
    'cyan': ['Cyan', '', 'mdi:flash'],
    'magenta': ['Magenta', '', 'mdi:flash'],
    'yellow': ['Yellow', '', 'mdi:flash'],
    'photoblack': ['Photoblack', '', 'mdi:flash'],
    'photocyan': ['Photocyan', '', 'mdi:flash'],
    'photomagenta': ['Photomagenta', '', 'mdi:flash'],
    'photoyellow': ['Photoyellow', '', 'mdi:flash'],
    'red': ['Red', '', 'mdi:flash'],
    'green': ['Green', '', 'mdi:flash'],
    'blue': ['Blue', '', 'mdi:flash'],
    'light_black': ['Light Black', '', 'mdi:flash'],
    'light_cyan': ['Light Cyan', '', 'mdi:flash'],
    'light_magenta': ['Light Magenta', '', 'mdi:flash'],
    'light_light_black': ['Light Light Black', '', 'mdi:flash'],
    'matte_black': ['Matte Black', '', 'mdi:flash'],
    'gloss_optimizer': ['Gloss Optimizer', '', 'mdi:flash'],
    'unknown': ['Unknown', '', 'mdi:flash'],
    'light_cyan_light_magenta_photoblack': ['Light Cyan, Light Magenta, Photoblack', '', 'mdi:flash'],
    '2x_grey_and_black': ['2x Grey and Black', '', 'mdi:flash'],
    'black_cyan_magenta_yellow': ['Black, Cyan, Magenta, Yellow', '', 'mdi:flash'],
    'photocyan_and_photomagenta': ['Photocyan and Photomagenta', '', 'mdi:flash'],
    'yellow_and_magenta': ['Yellow and Magenta', '', 'mdi:flash'],
    'cyan_and_black': ['Cyan and Black', '', 'mdi:flash'],
    'light_grey_and_photoblack': ['Light Grey and Photoblack', '', 'mdi:flash'],
    'light_grey': ['Light Grey', '', 'mdi:flash'],
    'medium_grey': ['Medium Grey', '', 'mdi:flash'],
    'photogrey': ['Photo Grey', '', 'mdi:flash'],
    'white': ['White', '', 'mdi:flash'],
}

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string,
    vol.Required(CONF_RESOURCES, default=[]):
        vol.All(cv.ensure_list, [vol.In(SENSOR_TYPES)]),
})


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Setup the ink level sensors."""
    scan_interval = config.get(CONF_SCAN_INTERVAL)
    host = config.get(CONF_HOST)

    try:
        data = InkLevelData(host)
    except requests.exceptions.HTTPError as error:
        _LOGGER.error(error)
        return False

    entities = []

    for color in config[CONF_RESOURCES]:
        sensor_type = color.lower()

        if sensor_type not in SENSOR_TYPES:
            SENSOR_TYPES[sensor_type] = [
                sensor_type.title(), '', 'mdi:flash']

        entities.append(InkSensor(data, sensor_type))

    add_entities(entities)


# pylint: disable=abstract-method
class InkLevelData(object):
    """Representation of Ink level."""

    def __init__(self, host):
        """Initialize the ink level."""
        self._host = host
        self.data = None

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        """Update the data from the printer."""
        try:
            cmd = subprocess.Popen('ink -b bjnp://{0}'.format(self._host), shell=True, stdout=subprocess.PIPE)
            levels = {}
            _LOGGER.debug("output: %s", cmd.stdout)
            for line in cmd.stdout:
                if b':' in line:
                    color, level = line.lower().split()
                    color = color.replace(' ', '_').replace(',', '')
                    levels[color] = level.replace('%', '')
            self.data = levels
            _LOGGER.debug("Data = %s", self.data)
        except requests.exceptions.RequestException:
            _LOGGER.error("Error occurred while fetching data.")
            self.data = None
            return False


class InkSensor(Entity):
    """Representation of a Ink Level sensor."""

    def __init__(self, data, sensor_type):
        """Initialize the sensor."""
        self.data = data
        self.type = sensor_type
        self._name = SENSOR_PREFIX + SENSOR_TYPES[self.type][0]
        self._unit = SENSOR_TYPES[self.type][1]
        self._icon = SENSOR_TYPES[self.type][2]
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return self._icon

    @property
    def state(self):
        """Return the state of the sensor. (percentage of ink left)"""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of this entity, if any."""
        return self._unit

    def update(self):
        """Get the latest data and use it to update our sensor state."""
        self.data.update()
        data = self.data

        self._state = data[self.type]