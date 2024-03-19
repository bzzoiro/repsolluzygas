"""Platform for sensor integration."""
from .repsol_api import RepsolLuzYGasSensor
from homeassistant.helpers.entity import Entity
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from datetime import timedelta
import requests
import logging

# Validation of the user's configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_USERNAME): cv.string,
    vol.Optional(CONF_PASSWORD): cv.string,
})

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(minutes=120)

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the sensor platform."""
    username = config[CONF_USERNAME]
    password = config[CONF_PASSWORD]

    client = RepsolLuzYGasSensor(username, password)
    add_entities([RepsolLuzYGazEntity(client, 'Amount', 'amount', '€', True),
                RepsolLuzYGazEntity(client, 'Consumption', 'consumption', 'kWh',  False),
                RepsolLuzYGazEntity(client, 'Total Days', 'totalDays', 'days',  False),
                RepsolLuzYGazEntity(client, 'Amount Variable', 'amountVariable', '€',  False),
                RepsolLuzYGazEntity(client, 'Amount Fixed', 'amountFixed', '€',  False),
                RepsolLuzYGazEntity(client, 'Average daily amount', 'averageAmount', '€',  False),
                RepsolLuzYGazEntity(client, 'Number of contracts', 'number_of_contracts', '',  False),
                RepsolLuzYGazEntity(client, 'Last invoice', 'last_invoice_amount', '€',  False),
                RepsolLuzYGazEntity(client, 'Last invoice was paid', 'last_invoice_paid', '',  False)], True)
                


class RepsolLuzYGazEntity(Entity):

    def __init__(self, client, name, variable, unit, is_master):

        _LOGGER.debug('Initalizing Entity testestestestste {}'.format(name))

        self.client = client
        self._name = name
        self.variable = variable
        self.is_master = is_master
        self.unit = unit


    @property
    def name(self):
        """Return the name of the sensor."""
        return 'Repsol - {}'.format(self._name)

    @property
    def state(self):
        """Return the state of the sensor."""
        _LOGGER.debug('Test1 {}'.format(self.client))

        data = self.client.data.get(self.variable, 0)
        _LOGGER.debug('{} has value: {}'.format(self._name, data))
        return data

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self.unit

    def update(self):
        """ This is the updater  """
        if self.is_master:
            _LOGGER.debug('Test2 {}'.format(self.client))
            self.client.update()
