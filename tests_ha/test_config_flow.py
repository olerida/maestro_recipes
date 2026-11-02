"""Test configuration using Home Assistant's real flow manager."""
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResultType
from pytest_homeassistant_custom_component.common import MockConfigEntry

DOMAIN = "maestro_recipes"
SOURCE = "maestro_mcz"


def add_source(hass, *, title="Stove account", entry_id="source1", available=True):
    source = MockConfigEntry(domain=SOURCE, title=title, entry_id=entry_id, data={})
    source.add_to_hass(hass)
    if available:
        hass.data.setdefault(SOURCE, {})[entry_id] = [SimpleNamespace(maestroapi=object())]
    return source


async def test_no_source(hass):
    result = await hass.config_entries.flow.async_init(DOMAIN, context={"source": config_entries.SOURCE_USER})
    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "no_source"


async def test_create_entry(hass):
    source = add_source(hass)
    result = await hass.config_entries.flow.async_init(DOMAIN, context={"source": config_entries.SOURCE_USER})
    assert result["type"] is FlowResultType.FORM
    with patch("custom_components.maestro_recipes.async_setup_entry", return_value=True) as setup:
        result = await hass.config_entries.flow.async_configure(result["flow_id"], {"source_entry_id": source.entry_id})
        await hass.async_block_till_done()
    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["data"] == {"source_entry_id": source.entry_id, "advanced": False}
    assert result["result"].unique_id == source.entry_id
    setup.assert_awaited_once()


async def test_error_recovery(hass):
    source = add_source(hass, available=False)
    result = await hass.config_entries.flow.async_init(DOMAIN, context={"source": config_entries.SOURCE_USER})
    result = await hass.config_entries.flow.async_configure(result["flow_id"], {"source_entry_id": source.entry_id})
    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {"base": "source_unavailable"}
    hass.data[SOURCE] = {source.entry_id: [SimpleNamespace(maestroapi=object())]}
    with patch("custom_components.maestro_recipes.async_setup_entry", return_value=True):
        result = await hass.config_entries.flow.async_configure(result["flow_id"], {"source_entry_id": source.entry_id})
        await hass.async_block_till_done()
    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["result"].unique_id == source.entry_id


async def test_already_configured_not_offered(hass):
    source = add_source(hass)
    MockConfigEntry(domain=DOMAIN, data={"source_entry_id": source.entry_id}, unique_id=source.entry_id).add_to_hass(hass)
    result = await hass.config_entries.flow.async_init(DOMAIN, context={"source": config_entries.SOURCE_USER})
    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "no_source"


async def test_multiple_accounts_only_unused_offered(hass):
    used = add_source(hass)
    unused = add_source(hass, entry_id="source2", title="Second account")
    MockConfigEntry(domain=DOMAIN, data={"source_entry_id": used.entry_id}, unique_id=used.entry_id).add_to_hass(hass)
    result = await hass.config_entries.flow.async_init(DOMAIN, context={"source": config_entries.SOURCE_USER})
    assert result["type"] is FlowResultType.FORM
    with patch("custom_components.maestro_recipes.async_setup_entry", return_value=True):
        result = await hass.config_entries.flow.async_configure(result["flow_id"], {"source_entry_id": unused.entry_id})
        await hass.async_block_till_done()
    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["result"].unique_id == unused.entry_id


async def test_failed_update_can_recover(hass):
    source = add_source(hass)
    coordinator = hass.data[SOURCE][source.entry_id][0]
    coordinator.last_update_success = False
    result = await hass.config_entries.flow.async_init(DOMAIN, context={"source": config_entries.SOURCE_USER})
    result = await hass.config_entries.flow.async_configure(result["flow_id"], {"source_entry_id": source.entry_id})
    assert result["errors"] == {"base": "source_unavailable"}
    coordinator.last_update_success = True
    with patch("custom_components.maestro_recipes.async_setup_entry", return_value=True):
        result = await hass.config_entries.flow.async_configure(result["flow_id"], {"source_entry_id": source.entry_id})
        await hass.async_block_till_done()
    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["result"].unique_id == source.entry_id


async def test_one_healthy_coordinator_suffices(hass):
    source = add_source(hass)
    coordinators = hass.data[SOURCE][source.entry_id]
    coordinators[0].last_update_success = False
    coordinators.append(SimpleNamespace(maestroapi=object(), last_update_success=True))
    result = await hass.config_entries.flow.async_init(DOMAIN, context={"source": config_entries.SOURCE_USER})
    with patch("custom_components.maestro_recipes.async_setup_entry", return_value=True):
        result = await hass.config_entries.flow.async_configure(result["flow_id"], {"source_entry_id": source.entry_id})
        await hass.async_block_till_done()
    assert result["type"] is FlowResultType.CREATE_ENTRY

async def test_advanced_selection_is_persisted(hass):
    source = add_source(hass)
    result = await hass.config_entries.flow.async_init(DOMAIN, context={"source": config_entries.SOURCE_USER})
    with patch("custom_components.maestro_recipes.async_setup_entry", return_value=True):
        result = await hass.config_entries.flow.async_configure(result["flow_id"], {"source_entry_id": source.entry_id, "advanced": True})
        await hass.async_block_till_done()
    assert result["data"] == {"source_entry_id": source.entry_id, "advanced": True}

@pytest.mark.parametrize(('data_value', 'options', 'expected'), [
    (False, {}, False),
    (True, {}, True),
    (True, {'advanced': False}, False),
    (False, {'advanced': True}, True),
])
async def test_options_default_respects_existing_mode(hass, data_value, options, expected):
    source = add_source(hass)
    entry = MockConfigEntry(domain=DOMAIN, data={'source_entry_id': source.entry_id, 'advanced': data_value}, options=options)
    entry.add_to_hass(hass)
    flow = await hass.config_entries.options.async_init(entry.entry_id)
    assert flow['type'] is FlowResultType.FORM
    assert flow['data_schema']({})['advanced'] is expected
