import logging
import requests
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

DOMAIN = "virgin_media_hub"
_LOGGER = logging.getLogger(__name__)

def setup(hass: HomeAssistant, config: dict):
    return True

def setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    hub = VirginMediaHub(entry.data)
    hass.data[DOMAIN] = hub
    hub.login()
    return True

def unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    hass.data.pop(DOMAIN)
    return True

class VirginMediaHub:
    def __init__(self, config):
        self.password = config["password"]
        self.base_url = "http://192.168.0.1"
        self.token = None

    def login(self):

        url = f"{self.base_url}/rest/v1/user/login"
        headers = {
            "Content-Type": "application/json",
            "Connection": "keep-alive"
        }

        data = {"password": self.password}

        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            self.token = response.json().get('token')
            _LOGGER.info("Successfully logged in to Virgin Media Hub")
        else:
            _LOGGER.error("Failed to log in to Virgin Media Hub")

    def get_active_clients(self):

        if not self.token:
            self.login()

        url = f"{self.base_url}/rest/v1/network/hosts?connectedOnly=true"

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Connection": "keep-alive"
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json().get('hosts', {}).get('hosts', [])
        else:
            _LOGGER.error("Failed to get active clients from Virgin Media Hub")
            return []
