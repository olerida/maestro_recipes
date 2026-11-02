"""Read-only recipe adjustments."""
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity import EntityCategory
from .entity import RecipeEntity, setup_read_entities
from .recipes import read_value


async def async_setup_entry(hass, entry, async_add_entities):
    """Discover recipe values now and on later coordinator updates."""
    setup_read_entities(entry, async_add_entities, RecipeSensor, ("pellet", "active_value"), int)


class RecipeSensor(RecipeEntity, SensorEntity):
    """A numeric recipe value reported by the source."""
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def native_value(self):
        value = read_value(self.stove, self.key)
        return value if type(value) is int else None
