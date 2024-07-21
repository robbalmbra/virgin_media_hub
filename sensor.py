from homeassistant.helpers.entity import Entity
from . import DOMAIN

async def async_setup_entry(hass, config_entry, async_add_entities):

    hub = hass.data[DOMAIN]
    sensors = []
    devices = hub.get_active_clients()

    for device in devices:

        sensors.append(VirginMediaHubClientSensor(device))

    async_add_entities(sensors, True)

class VirginMediaHubClientSensor(Entity):

    def __init__(self, device):

        self._device = device
        self._name = device['config'].get('hostname', 'Unknown device')
        self._state = device['config'].get('connected', False)

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def device_state_attributes(self):

        return {
            'mac_address': self._device.get('macAddress'),
            'ip_address': self._device['config']['ipv4'].get('address'),
            'interface': self._device['config'].get('interface'),
            'speed': self._device['config'].get('speed'),
            'ssid': self._device['config']['wifi'].get('ssid') if 'wifi' in self._device['config'] else None,
            'rssi': self._device['config']['wifi'].get('rssi') if 'wifi' in self._device['config'] else None,
            'band': self._device['config']['wifi'].get('band') if 'wifi' in self._device['config'] else None
        }

    def update(self):

        # In real implementation, fetch the latest data
        pass
