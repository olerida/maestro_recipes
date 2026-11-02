"""Recipe controls using a configured Maestro MCZ account."""
import asyncio
from dataclasses import dataclass
from homeassistant.const import Platform
from homeassistant.exceptions import ConfigEntryNotReady
from .const import SOURCE_DOMAIN

READ_PLATFORMS = [Platform.SENSOR, Platform.BINARY_SENSOR]
CONTROL_PLATFORMS = [Platform.NUMBER, Platform.SWITCH]


@dataclass
class RuntimeData:
    """Sources and the platforms actually loaded for this entry."""
    sources: list
    platforms: list


def get_sources(hass, entry_id):
    """Locate the tested legacy source coordinators."""
    entry = hass.config_entries.async_get_entry(entry_id)
    if entry is None or entry.domain != SOURCE_DOMAIN:
        return []
    source = hass.data.get(SOURCE_DOMAIN, {}).get(entry_id)
    if not isinstance(source, list):
        return []
    return [(coordinator, coordinator.maestroapi) for coordinator in source]


def sources_ready(sources):
    return any(getattr(coordinator, "last_update_success", True) for coordinator, _ in sources)


async def async_setup_entry(hass, entry):
    sources = get_sources(hass, entry.data["source_entry_id"])
    if not sources_ready(sources):
        raise ConfigEntryNotReady("Maestro MCZ source unavailable or unsupported")
    enabled = entry.options.get("advanced", entry.data.get("advanced", False))
    platforms = CONTROL_PLATFORMS if enabled else READ_PLATFORMS
    entry.runtime_data = RuntimeData(
        [(coordinator, stove, asyncio.Lock()) for coordinator, stove in sources],
        platforms,
    )
    await hass.config_entries.async_forward_entry_setups(entry, platforms)
    return True


async def async_unload_entry(hass, entry):
    return await hass.config_entries.async_unload_platforms(entry, entry.runtime_data.platforms)
