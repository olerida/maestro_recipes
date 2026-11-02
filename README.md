# Maestro MCZ Recipes

[Español](README.es.md)

Experimental Home Assistant integration for MCZ Maestro stove recipe controls. It reuses the account and cloud connection of [Maestro MCZ](https://github.com/Robbe-B/maestro_mcz). No additional credentials are required.

During setup, **Advanced options** is off by default and creates read-only entities. Enable it to use controls. To change the choice, remove and add the integration again.

Depending on model metadata, it can expose Pellet and Active adjustments, the Active switch, and adaptive mode. Numeric controls are restricted to the observed app range (−3 to +3) and any narrower model limits. Entities are created only for recognized sensor IDs, enabled configurations, types and valid limits. Values come from the source coordinator and may duplicate Maestro MCZ Extra Sensors entities.

Only the coordinator structure of Maestro MCZ **0.6.7-beta** is supported. Commands have been tested with mocks, not a physical stove. A successful HTTP response from the source integration does not establish that the device applied a change; check the subsequently refreshed state. This is an independent community project.

Install Maestro MCZ first. Copy `custom_components/maestro_recipes` to your Home Assistant `custom_components` directory, restart, add **Maestro MCZ Recipes** under Devices & Services and select the existing account. You may also add this repository as a custom HACS integration. Reload Recipes after reloading the source integration.

See [research notes](docs/investigacion.md). The code is licensed under MIT; MCZ branding belongs to its owner.

## Troubleshooting and removal

- If the account is missing, set up and load Maestro MCZ first. Each account can only be added once.
- If a value is missing, wait for a coordinator update and check disabled entities. Only fields supplied by the stove can appear.
- In advanced mode, controls are omitted when the model does not supply recognized identifiers, types or limits. Read-only entities do not require those metadata.
- For unavailable data, check the connection and Maestro MCZ. Reload Recipes after reloading the source integration.
- To remove it, open **Settings → Devices & services**, select Maestro MCZ Recipes and choose **Delete**. You can then remove its folder and restart. The Maestro MCZ account remains separate.

The [quality self-assessment](docs/bronze-review.md) describes the scope and remaining work; it is not an official certification.


Active changes refresh the source before sending both settings. This narrows, but cannot eliminate, races with Maestro+ or other clients because the source API does not expose an atomic conditional write. Avoid simultaneous changes.
