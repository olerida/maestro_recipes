"""Recipe adjustment numbers."""
from homeassistant.components.number import NumberEntity, NumberMode
from homeassistant.exceptions import HomeAssistantError
from .entity import RecipeEntity
from .recipes import discover, read_value


async def async_setup_entry(hass, entry, async_add_entities):
    entities = []
    for coordinator, stove, lock in entry.runtime_data.sources:
        commands = discover(stove.Model)
        for key in ("pellet", "active_value"):
            if key in commands and (key != "active_value" or "active_enabled" in commands):
                entities.append(RecipeNumber(coordinator, stove, lock, commands, key))
    async_add_entities(entities)


class RecipeNumber(RecipeEntity, NumberEntity):
    _attr_native_step = 1
    _attr_mode = NumberMode.SLIDER

    def __init__(self, coordinator, stove, lock, commands, key):
        super().__init__(coordinator, stove, lock, commands, key)
        self._attr_native_min_value = commands[key].minimum
        self._attr_native_max_value = commands[key].maximum
        self._attr_icon = "mdi:grain" if key == "pellet" else "mdi:tune-variant"

    @property
    def native_value(self):
        value = read_value(self.stove, self.key)
        return value if type(value) is int else None

    async def async_set_native_value(self, value):
        if not isinstance(value, (int, float)) or isinstance(value, bool) or not self._attr_native_min_value <= value <= self._attr_native_max_value or value != int(value):
            raise HomeAssistantError("Invalid recipe value")
        await self.send(int(value))
