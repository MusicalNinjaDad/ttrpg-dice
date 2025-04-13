# ttrpg-dice Changelog

## [v0.7.0] - 2025-04-13

### Added

- Allow `StatBlock` subtraction. For example, if you want to take an NPC and remove a specific career.

### Changed

- `StatBlock` algebra utilises the fact that `StatBlock` is a `Mapping`

## [v0.6.0] - 2025-04-06

### Breaking Changes

- Subclasses should override `_pre_init_`, overridden `__init__` cannot call `super()` due to updated mro.

## [v0.5.0] - 2025-04-05

### Changed

- Allow `StatBlock` subclasses to extend / override `__init__`
- `StatBlock`is a `Mapping`

### Added

- Statblock `str`, `repr` and `IPython.display`(as Markdown)

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
