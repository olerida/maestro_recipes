# Changelog

## 0.1.0

- Pin CI actions to immutable commits.
- Refresh Active settings before paired writes; concurrent external writes may still race.

- Read-only recipe values by default, with optional advanced controls during setup.
- Reuse an existing Maestro MCZ 0.6.7-beta account and coordinator.
- Restrict commands to recognized model metadata and serialize changes per stove.
- Discover late-arriving read-only values without additional polling and clean up listeners on unload.
- Validate model-family combinations and unavailable or invalid state before sending.
- Add local Bronze self-assessment and Home Assistant flow, lifecycle and simulated command tests; physical write operations remain unverified.
