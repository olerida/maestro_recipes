"""Select an existing Maestro MCZ account."""
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from . import get_sources, sources_ready
from .const import DOMAIN, SOURCE_DOMAIN


class MaestroRecipesConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    @callback
    def _async_current_ids(self):
        return {entry.data.get("source_entry_id") for entry in self._async_current_entries()}

    async def async_step_user(self, user_input=None):
        errors = {}
        entries = {entry.entry_id: entry.title for entry in self.hass.config_entries.async_entries(SOURCE_DOMAIN) if entry.entry_id not in self._async_current_ids()}
        if not entries:
            return self.async_abort(reason="no_source")
        if user_input is not None and user_input.get("source_entry_id") in entries:
            source = user_input["source_entry_id"]
            if not sources_ready(get_sources(self.hass, source)):
                errors["base"] = "source_unavailable"
            else:
                await self.async_set_unique_id(source)
                self._abort_if_unique_id_configured()
                return self.async_create_entry(title=entries[source], data={"source_entry_id": source, "advanced": user_input.get("advanced", False)})
        return self.async_show_form(step_id="user", data_schema=vol.Schema({vol.Required("source_entry_id"): vol.In(entries), vol.Optional("advanced", default=False): bool}), errors=errors)
