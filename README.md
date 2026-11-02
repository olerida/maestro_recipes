# Maestro MCZ Recipes

<img src="custom_components/maestro_recipes/brand/icon.png" alt="Maestro MCZ Recipes" width="128">

[Español](README.es.md)

Maestro MCZ Recipes is a custom integration for [Home Assistant](https://www.home-assistant.io/) that displays recipe settings from MCZ Maestro stoves. Optional controls can adjust Active, Pellet and adaptive mode. It uses the existing [Maestro MCZ integration](https://github.com/Robbe-B/maestro_mcz) and does not require additional credentials.

This integration is experimental. Commands have been tested with simulations, but **their application on a physical stove has not yet been verified**. See the [research notes](docs/investigacion.md) and [quality self-assessment](docs/bronze-review.md); the latter is not an official rating.

Local MCZ branding is included for Home Assistant 2026.3 or newer.

## Supported devices

The code supports the coordinator structure of **Maestro MCZ 0.6.7-beta**. The app screens were investigated using Maestro+ 5.6.9 and an MCZ Ego Comfort Air with M2S.AIR.24.20 firmware. Physical writes and full compatibility with other stoves or source-integration versions have not been verified.

## Prerequisites

1. Configure the stove in the Maestro+ MCZ app and verify that it is connected.
2. Install and configure [Maestro MCZ](https://github.com/Robbe-B/maestro_mcz) in Home Assistant and check that it detects the stove.
3. Ensure the original integration can reach the MCZ cloud.

## Installation

### Manual installation

1. Copy `custom_components/maestro_recipes` from this repository into the `custom_components` directory of your Home Assistant configuration. Create the directory if necessary.
2. Restart Home Assistant.

### HACS

[![Open this integration in Home Assistant Marketplace](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=olerida&repository=maestro_recipes&category=integration)

The button opens the dialog to add the custom repository in HACS. You can also add it manually:

1. In HACS, open **Integrations** and choose **Custom repositories** from the menu.
2. Add `https://github.com/olerida/maestro_recipes` with category **Integration**.
3. Find **Maestro MCZ Recipes**, download it and restart Home Assistant.

This is a custom repository and is not included in the default HACS catalog. No tagged release has been published yet; download availability depends on HACS version options. Manual installation uses the code on `main`.

## Updating

Install an available update from HACS and restart Home Assistant. For a manual installation, replace the integration directory with the desired version and restart. Review the [changelog](CHANGELOG.md) before updating.

## Configuration

1. In Home Assistant, open **Settings** → **Devices & services**.
2. Select **Add integration** and search for **Maestro MCZ Recipes**.
3. Select the account already configured in Maestro MCZ.
4. Leave **Advanced options** unchecked to view values without controls. Enable it to expose supported controls, then submit.

No additional credentials are required. Each Maestro MCZ account can be added once. To change the advanced setting, remove and add the integration again.

## Supported functionality

| App setting | Read-only mode | With advanced options |
|---|---|---|
| Active | Adjustment and enabled state | Adjustment and enable/disable |
| Pellet | Adjustment | Adjustment |
| Adaptive mode | State | Enable/disable |

Read-only entities appear only when the original integration supplies a value. Controls appear only when the stove's model metadata contains recognized identifiers, types and limits. Numeric adjustments are restricted to the range observed in Maestro+ (−3 to +3) and any narrower model limits. Some values may duplicate Maestro MCZ Extra Sensors entities.

## Data updates and commands

The integration reads values from the existing Maestro MCZ coordinator; the original integration controls the update interval. Advanced controls send commands through that integration and request a subsequent refresh.

Changing Active refreshes the source and sends the adjustment and enabled state together. This reduces, but cannot eliminate, races if Maestro+ or another client changes a setting at the same time. Avoid simultaneous changes and check the refreshed state: an accepted response does not by itself prove that the stove applied the command.

## Known limitations

- This is an independent community project, not an official MCZ integration.
- Commands have not been validated on a physical stove; controls are experimental.
- Values must be provided by the original integration, and controls must be recognized for the model.
- The component uses internal Maestro MCZ interfaces that may change. Only the 0.6.7-beta coordinator structure is supported.
- Reload Recipes after reloading or updating Maestro MCZ.
- The setup form and entity names are available in English and Spanish.

## Troubleshooting

- **No account is available:** configure Maestro MCZ first and check that it is loaded. Each account can be added once.
- **A value is missing:** wait for a coordinator update and check disabled entities. The stove and source integration must provide the data.
- **A control is missing:** check that **Advanced options** is enabled. Controls also require recognized model metadata and valid numeric limits.
- **Values are unavailable or stale:** check the stove connection and Maestro MCZ. Reload Recipes after reloading the original integration.
- **HACS does not show a version:** check the repository's version options. If no release is available, use manual installation.

## Remove the integration

Open **Settings** → **Devices & services**, select **Maestro MCZ Recipes**, open its menu and select **Delete**. To remove the files as well, delete `custom_components/maestro_recipes` and restart Home Assistant. The original Maestro MCZ integration and its account are separate.

## License

The project code is distributed under the [MIT License](LICENSE). The Maestro+ icon and MCZ trademarks belong to their owner and are not covered by the MIT license.
