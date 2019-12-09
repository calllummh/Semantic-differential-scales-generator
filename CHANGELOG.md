# [Future versions]
### To be added
Adding functionality to import CSV files to read data.


# [Unreleased]
## 2019-12-09
### Changed
Moved make_graph method inside Property class in the interest of optimisation. Results in less parameters required to be passed in, as array data, and name are already contained within the method.
### Removed
Removed mat_values method from Property, as it was obsolte, and was superseded by Property Values class.


# V3.3
## 2019-12-09
### Fixed
Graph now features rotated text to avoid cluttering of the axes.

# V3.2
## 2019-12-07
### Fixed
Functionality in FilePath class to make safe_file_name function correctly.

# V3.1
## 2019-12-07
### Fixed
Huge bug in while loop structure causing user to be stuck in an eternal loop.


# V3.0
## 2019-12-07
### Added
Added functionality to generate CSV files for each plot.
### Changed
Changed functionality of file path generation within code to use a FilePath class.
### Fixed
Bug where if a / was included in the property name, python's generation of the .png file would fail due to pathing error.


# V2.0
## 2019-12-07
### Added
File writing of plots to a new or existing directory based on working directory when script is run.
### Removed
Functionality of showing plots when script is run.


# V1.0
## 2019-12-06
### Added
Uploaded version 1.0
