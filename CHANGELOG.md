# ttrpg-dice Changelog

## [v0.4.0] - 2025-03-30

### Added

- Create a `Dice` from a `str`ing in ndx notation (e.g. `d.from_str("2d4 + 3")`)

## [v0.3.0] - 2025-03-30

### Breaking Changes

- Directly subclass a specific `StatBlock` without using the `@statblock` decorator to create a specific set of stats as a class
- `StatBlock` is no longer a `dataclass`

## [v0.2.0] - 2025-03-14

### Added

- `StatBlock` class (docs to follow)
