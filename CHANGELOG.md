# Change Log
All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/).

## [Unreleased]
### Changed
- Using [flake8](http://flake8.pycqa.org/) package for code validation.
- Restructored project.

## [0.0.14] - 2015-07-05
### Added
- Brute Force Fitter class.

## [0.0.13] - 2015-07-04
### Added
- Docstrings for main classes.
### Fixed
- Gibbs Sampler Fitter loops count control.
- Gibbs Sampler Fitter loops endings.
- Images difference measure.

## [0.0.12] - 2015-06-26
### Added
- Gibbs Sampler Fitter class.
- Ability to change one coefficient of face.

## [0.0.11] - 2015-06-24
### Added
- Separate class for Nelder-Mead fitting.

### Changed
- Made `ModelFitter` class abstract.

### Fixed
- MFM uses C function for random Face generation.

## [0.0.10] - 2015-06-23
### Added
- Nelder-Mead method for model form fitting.
- Controls to launch fitting procedure.

### Changed
- Name of light estimate method in `ModelFitter`.
- Improved performance of Face generation.

## [0.0.9] - 2015-06-15
### Added
- Ability to change directed light properties by keyboard.
- Fitter class with ability to find best fitting light conditions.

### Changed
- Model uses View, instead of constituting composite.

## [0.0.8] - 2015-06-06
### Added
- ModelInput class.

## [0.0.7] - 2015-06-06
### Added
- Model class.

## [0.0.6] - 2015-06-05
### Changed
- Improved normal map calculation performance.

## [0.0.5] - 2015-06-01
### Added
- View class.

## [0.0.4] - 2015-05-31
### Added
- MFM (Morphable Face Model) singleton.
- Added style checkers to dependencies.

## [0.0.3] - 2015-05-29
### Added
- Integration with [travis-ci](https://travis-ci.org/char-lie/mfm).
- Integration with [coveralls](https://coveralls.io/github/char-lie/mfm).

## [0.0.2] - 2015-05-29
### Added
- `Face` class.
- Unit tests.

### Fixed
- Link in CHANGELOG.

## 0.0.1 - 2015-05-23
### Added
- Basic MFM example, which can following:
 - load the model from MatLab file;
 - generate random face;
 - display the model;
 - rotate the model;
 - use normal map or light map as a texture.

### Removed
- All code from
  [patterns recognition](https://github.com/char-lie/patterns_recognition)
  repository, which doesn't belong to this one.

[Unreleased]: https://github.com/char-lie/mfm/compare/v0.0.14...HEAD
[0.0.14]: https://github.com/char-lie/mfm/compare/v0.0.13...v0.0.14
[0.0.13]: https://github.com/char-lie/mfm/compare/v0.0.12...v0.0.13
[0.0.12]: https://github.com/char-lie/mfm/compare/v0.0.11...v0.0.12
[0.0.11]: https://github.com/char-lie/mfm/compare/v0.0.10...v0.0.11
[0.0.10]: https://github.com/char-lie/mfm/compare/v0.0.9...v0.0.10
[0.0.9]: https://github.com/char-lie/mfm/compare/v0.0.8...v0.0.9
[0.0.8]: https://github.com/char-lie/mfm/compare/v0.0.7...v0.0.8
[0.0.7]: https://github.com/char-lie/mfm/compare/v0.0.6...v0.0.7
[0.0.6]: https://github.com/char-lie/mfm/compare/v0.0.5...v0.0.6
[0.0.5]: https://github.com/char-lie/mfm/compare/v0.0.4...v0.0.5
[0.0.4]: https://github.com/char-lie/mfm/compare/v0.0.3...v0.0.4
[0.0.3]: https://github.com/char-lie/mfm/compare/v0.0.2...v0.0.3
[0.0.2]: https://github.com/char-lie/mfm/compare/v0.0.1...v0.0.2
