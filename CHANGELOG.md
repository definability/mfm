# Change Log
All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/).

## [Unreleased]
### Added
- Ability to set following static fields to `View`
  - principal components via `set_principal_components`;
  - deviations of principal components via `set_deviations`.

### Changed
- `get_face` method has `coefficients_only` parameter to set
    whether it's needed to calculate the face;
- Assertion in `ShadersHelper` if uniform matrix binding failed.

### Deprecated
- `C` modules are deprecated because shaders will do all work
  - `face`;
    - `calculate_face`;
    - `calculate_row`;
  - `normals`;
    - `get_normals`.
- Face
  - `normal_map_to_normal_vectors` will not be needed
    because of new shadows model;
  - `normalize` will not be needed because shaders will zoom out the model;
  - `get_original_vertices` will not be neede;
    beause will be calculated by shaders;
  - `get_vertices` will not be needed
    beause will be calculated by shaders;
  - `get_triangles_c` because `OpenGL` doesn't need C array of triangles.

## [0.2.1] - 2016-08-01
### Added
- Face properties with setters and getters
  - `directed_light`;
  - `ambient_light`;
  - `light`;
- View properties with setters and getters
  - `light`;
  - `normals`;
  - `vertices`;
  - `colors`;
  - `rotation`.

### Changed
- Vertex shader calculates normal map or shadow depending on input.

### Deprecated
- Usage of normal maps: shadows will be calculated in shaders
  and normal map will be redundant for shadow calculations via
  least squares method;
- Face
  - `get_vertices_c` not needed;
  - `get_directed_light` has shortcut property `directed_light`;
  - `get_constant_light` has shortcut property `ambient_light`;
  - `get_light_map` not needed;
  - `get_light_map_c` not needed;
  - `get_normal_map_c` not needed;
  - `get_normal_map` not needed;
  - `set_light` has shortcut properties `directed_light` and `ambient_light`;
- View
  - `update` has shortcut properties `light`, `normals`, `vertices`,
    `colors` and `rotation`.

## [0.2.0] - 2016-07-31
### Changed
- Using shaders for face rendering.

## [0.1.0] - 2016-07-31
### Added
- Ability to set initial values of coefficients for Fitters.

### Changed
- Calculating derivatives from two sides in BGD Fitter.

### Fixed
- Loops count in BGD Fitter.
- Saving result in Nelder-Mead Fitter.
- Saving result in BGD Fitter.

## [0.0.19] - 2016-07-18
### Changed
- Default parameters for BGD Fitter.
- Type of counters in C modules changed to size\_t.

### Fixed
- Ability to specify not all coefficients for Face calculation.

## [0.0.18] - 2016-07-14
### Added
- Batch Gradient Descent Fitter.

### Changed
- Added ability to not use all PC coefficients for `Face` calculation.

## [0.0.17] - 2016-07-11
### Changed
- Made bump script to not depend on Python packages.

## [0.0.16] - 2016-07-11
### Added
- Bash script to bump application version.

## [0.0.15] - 2015-07-10
### Changed
- Using [flake8](http://flake8.pycqa.org/) package for code validation.
- Restructured project.
- Using [setuptools](https://setuptools.readthedocs.io/en/latest/)
    to build and test the application.

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

[Unreleased]: https://github.com/char-lie/mfm/compare/v0.2.1...HEAD
[0.2.1]: https://github.com/char-lie/mfm/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/char-lie/mfm/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/char-lie/mfm/compare/v0.0.19...v0.1.0
[0.0.19]: https://github.com/char-lie/mfm/compare/v0.0.18...v0.0.19
[0.0.18]: https://github.com/char-lie/mfm/compare/v0.0.17...v0.0.18
[0.0.17]: https://github.com/char-lie/mfm/compare/v0.0.16...v0.0.17
[0.0.16]: https://github.com/char-lie/mfm/compare/v0.0.15...v0.0.16
[0.0.15]: https://github.com/char-lie/mfm/compare/v0.0.14...v0.0.15
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
