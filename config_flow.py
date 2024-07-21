import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback

from . import DOMAIN

class VirginMediaHubConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="Virgin Media Hub", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("password"): str,
            })
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return VirginMediaHubOptionsFlow(config_entry)

class VirginMediaHubOptionsFlow(config_entries.OptionsFlow):

    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required("password", default=self.config_entry.data.get("password")): str,
            })
        )
