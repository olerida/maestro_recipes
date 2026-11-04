# Changelog

## 0.1.3

- Fix the README image URL when displayed in HACS.

## 0.1.2

- Warn beside advanced options during setup and configuration that controls can modify combustion settings and are intended for technicians or people with advanced knowledge.
- Clarify that normal mode is read-only in the English and Spanish README files.

## 0.1.1

- Change advanced options from Configure without removing the integration or reconnecting the account.
- Reload the correct platforms when switching between read-only and control modes.

## 0.1.0

- Pin CI actions to immutable commits.
- Refresh Active settings before paired writes; concurrent external writes may still race.

- Read-only recipe values by default, with optional advanced controls during setup.
- Reuse an existing Maestro MCZ 0.6.7-beta account and coordinator.
- Restrict commands to recognized model metadata and serialize changes per stove.
- Discover late-arriving read-only values without additional polling and clean up listeners on unload.
- Validate model-family combinations and unavailable or invalid state before sending.
- Add local Bronze self-assessment and Home Assistant flow, lifecycle and simulated command tests; physical write operations remain unverified.
