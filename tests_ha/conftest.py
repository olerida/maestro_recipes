"""Home Assistant test fixtures."""
from pathlib import Path
import pytest
from unittest.mock import AsyncMock
from pytest_homeassistant_custom_component.common import MockModule, mock_integration


@pytest.fixture(autouse=True)
def integration_in_hass_config(hass, enable_custom_integrations):
    """Make the integration discoverable in the isolated HA config."""
    mock_integration(hass, MockModule("maestro_mcz", async_setup=AsyncMock(return_value=True)))
    link = Path(hass.config.config_dir) / "custom_components" / "maestro_recipes"
    link.symlink_to(Path(__file__).parents[1] / "custom_components" / "maestro_recipes", target_is_directory=True)
    yield
    link.unlink()
