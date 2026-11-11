"""Recipe controls using a configured Maestro MCZ account."""
import asyncio
from collections.abc import Mapping
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
    """Locate stoves by capability across known source layouts."""
    entry = hass.config_entries.async_get_entry(entry_id)
    if entry is None or entry.domain != SOURCE_DOMAIN:
        return []
    source = getattr(entry, "runtime_data", None)
    if source is None:
        source = hass.data.get(SOURCE_DOMAIN, {}).get(entry_id)
    if isinstance(source, Mapping):
        coordinators = source.values()
    elif isinstance(source, (list, tuple)):
        coordinators = source
    else:
        stoves = getattr(source, "stoves", None)
        if isinstance(stoves, Mapping):
            return [(source, stove) for stove in stoves.values() if stove is not None]
        coordinators = (source,)
    result = []
    for coordinator in coordinators:
        stove = getattr(coordinator, "stove", None) or getattr(coordinator, "maestroapi", None)
        if stove is not None:
            result.append((coordinator, stove))
    return result


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
