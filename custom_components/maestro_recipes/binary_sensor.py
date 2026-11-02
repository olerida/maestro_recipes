"""Read-only recipe switches."""
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.helpers.entity import EntityCategory
from .entity import RecipeEntity, setup_read_entities
from .recipes import read_value


async def async_setup_entry(hass, entry, async_add_entities):
    """Discover recipe values now and on later coordinator updates."""
    setup_read_entities(entry, async_add_entities, RecipeBinarySensor, ("adaptive", "active_enabled"), bool)


class RecipeBinarySensor(RecipeEntity, BinarySensorEntity):
    """A boolean recipe value reported by the source."""
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def is_on(self):
        value = read_value(self.stove, self.key)
        return value if type(value) is bool else None
