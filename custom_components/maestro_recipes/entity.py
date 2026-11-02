"""Shared state and serialized command handling."""
from homeassistant.core import callback
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .recipes import read_value


def setup_read_entities(entry, async_add_entities, entity_class, keys, value_type):
    """Create entities when values first appear and release listeners on unload."""
    for coordinator, stove, lock in entry.runtime_data.sources:
        known = set()

        @callback
        def discover(coordinator=coordinator, stove=stove, lock=lock, known=known):
            new = []
            for key in keys:
                if key not in known and type(read_value(stove, key)) is value_type:
                    known.add(key)
                    new.append(entity_class(coordinator, stove, lock, {}, key))
            if new:
                async_add_entities(new)

        discover()
        entry.async_on_unload(coordinator.async_add_listener(discover))


class RecipeEntity(CoordinatorEntity):
    _attr_has_entity_name = True
    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, coordinator, stove, lock, commands, key):
        super().__init__(coordinator)
        self.stove, self.lock, self.commands, self.key = stove, lock, commands, key
        self._attr_unique_id = f"{stove.UniqueCode}-recipe-{key}"
        self._attr_translation_key = key
        self._attr_device_info = coordinator.get_device_info()

    @property
    def available(self):
        connected = getattr(getattr(self.stove, "Status", None), "is_connected", None)
        value = read_value(self.stove, self.key)
        expected = int if self.key in ("pellet", "active_value") else bool
        if type(value) is not expected:
            return False
        if self.commands and self.key.startswith("active_"):
            return super().available and connected is not False and value is not None and all(read_value(self.stove, k) is not None for k in ("active_value", "active_enabled"))
        return super().available and connected is not False and value is not None

    async def send(self, value):
        from custom_components.maestro_mcz.maestro.http.request import MczProgramCommand

        async with self.lock:
            if not self.available:
                raise HomeAssistantError("Stove or current recipe state is unavailable")
            if self.key.startswith("active_"):
                # Refresh before reading the other setting; this cannot make the
                # read and write atomic across the app and other integrations.
                await self.coordinator.async_refresh()
                if not self.available:
                    raise HomeAssistantError("Could not refresh current Active settings")
            values = {self.key: value}
            if self.key.startswith("active_"):
                other = "active_enabled" if self.key == "active_value" else "active_value"
                values[other] = read_value(self.stove, other)
                if type(values["active_enabled"]) is not bool or type(values["active_value"]) is not int:
                    raise HomeAssistantError("Current Active settings are invalid")
                bounds = self.commands["active_value"]
                if not bounds.minimum <= values["active_value"] <= bounds.maximum:
                    raise HomeAssistantError("Current Active value is outside model limits")
            config_ids = {self.commands[k].config_id for k in values}
            if len(config_ids) != 1:
                raise HomeAssistantError("Recipe commands use incompatible configurations")
            commands = [MczProgramCommand(self.commands[k].sensor_id, v) for k, v in values.items()]
            accepted = False
            def success():
                nonlocal accepted
                accepted = True
            await self.stove.ActivateProgramMultipleCommands(config_ids.pop(), commands, success)
            if not accepted:
                raise HomeAssistantError("Maestro MCZ did not confirm the request")
            await self.coordinator.update_data_after_set()
