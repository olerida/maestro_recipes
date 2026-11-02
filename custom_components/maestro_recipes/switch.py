"""Recipe switches."""
from homeassistant.components.switch import SwitchEntity
from .entity import RecipeEntity
from .recipes import discover, read_value


async def async_setup_entry(hass, entry, async_add_entities):
    entities = []
    for coordinator, stove, lock in entry.runtime_data.sources:
        commands = discover(stove.Model)
        for key in ("adaptive", "active_enabled"):
            if key in commands and (key != "active_enabled" or "active_value" in commands):
                entities.append(RecipeSwitch(coordinator, stove, lock, commands, key))
    async_add_entities(entities)


class RecipeSwitch(RecipeEntity, SwitchEntity):
    _attr_icon = "mdi:toggle-switch"

    @property
    def is_on(self):
        value = read_value(self.stove, self.key)
        return value if type(value) is bool else None

    async def async_turn_on(self, **kwargs):
        await self.send(True)

    async def async_turn_off(self, **kwargs):
        await self.send(False)
