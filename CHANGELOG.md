# mikeio1d Changelog

## [Unreleased]

### Added

### Fixed

### Changed

### [0.8.2] - 2024-10-14

### Fixed

- Derived quantities were missing from object html representations.

### [0.8.1] - 2024-10-14

### Fixed

- Wheel and source builds did not include all necessary binary dependencies.

## [0.8.0] - 2024-10-14

### Added

- Derived quantity concept introduced with an API the same as regular quantities.
- Nine default derived quantities (e.g. 'Node Flooding', 'Reach Filling', etc.).
- Ability to extend MIKE IO 1D with custom derived quantities.
- Quantity units are now more consistently visible in object representations.

### Fixed

- Fixed bug where rounding to milliseconds sometimes failed.

### Changed

- Updated documentation and README examples.


## [0.7.0] - 2024-09-19

### Added

- New API for reading and writing xns11 files (see new notebook examples).
- Access to both raw and processed data in xns11 files.
- Export xns11 sections and markers to GeoPandas.
- Gridpoint indexing from ResultReach by either chainage or number.
- Extra gridpoint static attributes: chainage, reach name, and x/y coordinates.

### Fixed

- Various warning fixes related to new Pandas and GeoPandas versions.

### Changed

- Removed support for Python 3.8 (to be compatible with Pandas >= 2.1).
- Iterating over IRes1DReach objects must now be done via ResultReach.reaches.


## [0.6.1] - 2024-03-23

### Fixed

- Loading MIKE IO 1D together with MIKE+Py
- Fixed override_name parameter that was not working in ResultFrameAggregator
- Fixed converting res11 to res1d
- Fixed calling ResultQuantityCollection.plot with kwargs

## [0.6] - 2024-02-08

### Added

- Introduced TimeSeriesId to uniquely identify results.
- Read methods now include 'column_mode' parameter that enables multiindex reading (e.g. column_mode='compact').
- Added more type hints to improve IDE auto-completion and docstring peeking.
- Merging of regular and LTS extreme/periodic res1d files.
- Convert reaches to GeoPandas in two modes: 'segmented' and 'combined'.
- Export to GeoPandas with quantities aggregated in time.

### Changed

- Result reading/writing fundamentally uses TimeSeriesId now instead of QueryData
- DataFrames previously including duplicates are now resolved by TimeSeriesId (especially for reach segments, the 'tag' level is used)
- Following are now abstract base classes: ResultReader, QueryData, ResultLocation
- GeoPandas conversion now includes extra columns matching some TimeSeriesId fields.

## [0.5] - 2023-12-22

### Added

- Support for Python 3.12
- Linux support (experimental).
- Initial support for GeoPandas (ability to export static network)
- Geometry package for converting IRes1DLocation objects to corresponding Shapely objects
- Updated documentation hosted on GitHub Pages.

### Fixed

### Changed

- Consistent and pythonic test file structure

## [0.4.1] - 2023-12-14

### Added

- mikenet module for easier work with DHI .NET libraries.

### Fixed

- Res1D filtering for reaches inside MIKE 1D itself.

### Changed

- Use MIKE 1D NuGet packages v22.0.3 and v22.0.4 for DHI.Mike1D.ResultDataAccess

## [0.4] - 2023-09-14

### Added

- DHI.Mike1D.MikeIO C# utility and ResultReaderCopier for more performant reading of result files

### Changed

- Made ResultQuantity.plot method more Matplotlib-like

### Fixed

- Reading of MOUSE results files: CRF, PRF, and XRF
- Include milliseconds from .res1d files

### Removed

- Support for Python 3.6

## [0.3] - 2023-04-21

### Added

- Ability to add queries using auto-completion
- Ability to modify res1d file contents using a data frame
- Ability to extract time series to csv, dfs0, and txt files
- Support for querying structures and global data items

### Changed

- Use MIKE 1D NuGet packages v21.0.0

## [0.2] - 2023-03-14

### Added

- Ability to read result files in a filtered way
- More detailed information about result files in __repr__
- Dictionaries containing catchment, node, reach, and global result item classes
- Support for reading SWMM and EPANET result files by upgrading to MIKE 1D v20.1.0
- Support for reading LTS result files

### Changed

- Use MIKE 1D NuGet packages v20.1.0
- Use Python.NET v3.0.1

### Fixed

- Fix data frame fragmentation error for res1d with many columns

### Removed

- .NET and native DHI libraries from source control

## [0.1] - 2021-05-05

### Added

- Reading of res1d and xns11 files into pandas data frames


[unreleased]: https://github.com/DHI/mikeio1d/compare/v0.8.0...HEAD
[0.8.0]: https://github.com/DHI/mikeio1d/releases/tag/v0.8.0
[0.7.0]: https://github.com/DHI/mikeio1d/releases/tag/v0.7.0
[0.6.1]: https://github.com/DHI/mikeio1d/releases/tag/v0.6.1
[0.6]: https://github.com/DHI/mikeio1d/releases/tag/v0.6
[0.5]: https://github.com/DHI/mikeio1d/releases/tag/v0.5
[0.4.1]: https://github.com/DHI/mikeio1d/releases/tag/v0.4.1
[0.4]: https://github.com/DHI/mikeio1d/releases/tag/v0.4
[0.3]: https://github.com/DHI/mikeio1d/releases/tag/v0.3
[0.2]: https://github.com/DHI/mikeio1d/releases/tag/v0.2
[0.1]: https://github.com/DHI/mikeio1d/releases/tag/v0.1
