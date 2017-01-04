# Change Log
All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/).

## [Unreleased]
### Added
- `libs` package (`C` modules) which were removed in [0.3.0]
  - `face`;
    - `calculate_face`;
    - `calculate_row`;
  - `normals`;
    - `get_normals`.

### Fixed
- Flat shadows moved from its place on model when had to stay fixed.
- Shadow map model was projected instead of being rotated.

### Changed
- Rotating camera instead of model (rotation doesn't affect shadows)
  - allows to not recalculate shadows on rotation;
  - simplifies visual check of proper movement rendering.
- Smooth shadows.

### Removed
- `Texture` enumerate from `Model` module as not used.
- Shape and normals calculations from shaders in favor of `C` modules.

## [0.7.2] - 2016-12-29
### Removed
- `ShadersHelper` `bind_uniform_ints` method in favor of `bind_uniform_array`.
- `ShadersHelper` `bind_uniform_floats` method in favor of `bind_uniform_array`.

### Added
- `ShadersHelper` `bind_uniform_array` method.

## [0.7.1] - 2016-12-28
### Added
- Logging setup via command line arguments.

### Changed
- Fitting configuration file became optional.

## [0.7.0] - 2016-12-27
### Added
- `Face` rotation parameters.
- `Face` convertion to `NumPy` `array`.

### Fixed
- `Face` PC `cefficients` should have type of `NumPy` `array`.

### Changed
- `Face` save saves entire `Face` as `NumPy` `array` to file.
- `Face` rotation and light are represented in spherical coordinates.
- `ModelFitter` calculates `Face` dimensions got from constants.
- Fitters work with new `Face` and `ModelFitter`
    - Batch gradient descent;
    - Brute force;
    - Gibbs sampler;
    - Monte-Carlo;
    - Nelder-Mead.

### Removed
- `Face` ambient light as an image option.

## [0.6.0] - 2016-11-03
### Changed
- Using shadow mapping.

### Fixed
- MFM loading from `.npz` and `.mat` file.

## [0.5.5] - 2016-11-03
### Added
- Ability to load MFM from `.npz` file.
- Error if MFM file was not found.

## [0.5.4] - 2016-11-02
### Fixed
- `MonteCarloFitter` initial image normalization.
- `MonteCarloFitter` Face pixels check.
- `View` alpha channel storing.

## [0.5.3] - 2016-10-19
### Added
- Monte Carlo Fitter class.

## [0.5.2] - 2016-10-10
### Added
- Final callback to `NelderMeadFitter` constructor.

### Fixed
- `NelderMeadFitter` parameters passing.
- `BruteForceFitter` final processing.

## [0.5.1] - 2016-09-09
### Fixed
- `BruteForceFitter` to work with levels starting not from `0`.

## [0.5.0] - 2016-09-08
### Fixed
- `GibbsSamplerFitter` to work with new `ModelFitter` interface.

## [0.4.12] - 2016-09-05
### Fixed
- Image flip on save.
- Derivative for light component in `BGDFitter`.

## [0.4.11] - 2016-09-04
### Added
- Command line arguments processing.
- [JSON](http://www.json.org/) configuration files processing
    to handle fitting procedure.

### Changed
- `ModelInput` saves files to `output` directory to avoid garbage.

## [0.4.10] - 2016-09-04
### Fixed
- Input image flip in example.

## [0.4.9] - 2016-09-04
### Added
- `FittersChain` class for handy creation of fitters sequences.
- `callback` parameter to `ModelFitter` constructor.
- `callback` parameter to `BruteForceFitter` constructor.
- `finish` method to `ModelFitter`.
- `finish` method to `BruteForceFitter`.

### Changed
- `ModelFitter` constructor corrects `initial_face`
    according to provided amount of dimensions.

## [0.4.8] - 2016-08-28
### Added
- `levels` parameter in `BruteForceFitter` constructor.

### Removed
- `max_level` parameter from constructor of `BruteForceFitter`
    in favor of `levels`.

## [0.4.7] - 2016-08-28
### Added
- `light_dx` parameter to `BGDFitter` constructor
    to handle derivation of light components.
- `initial_face` parameter to `BruteForceFitter` constructor.

## [0.4.6] - 2016-08-28
### Added
- Images formats libraries installation for Pillow.

### Fixed
- Model scaling when it's not rotating.

## [0.4.5] - 2016-08-25
### Added
- `bind_uniform_ints` method in `ShadersHelper` to bind array if integers.
- Ability to choose coefficients to be calculated in vertices shader.

## [0.4.4] - 2016-08-23
### Fixed
- `ModelFitter` image deviation calculator should work without normals.

## [0.4.3] - 2016-08-22
### Fixed
- Removed call of non-existent texture toggle from `ModelInput`.

## [0.4.2] - 2016-08-22
### Fixed
- `View` should accept `NumPy` array of triangles to display `Face` properly.

## [0.4.1] - 2016-08-17
### Fixed
- Principal components amount in vertex shader for face.

## [0.4.0] - 2016-08-17
### Removed
- `ModelFitter`
  - `request_normals` in favor of `request_image`;
  - `receive_normals` in favor of `receive_image`;
  - `estimate_light` will be useless with shadow mapping.
- `Face`
  - `set_triangles` useless because `View` has triangles.
- `View`
  - `update` in favor of `light`, `normals`, `vertices`,
  - `normals` useless with shaders;
  - `vertices` useless with shaders;
  - `colors` useless with shaders.
- `libs` package (`C` modules) are useless with shaders
  - `face`;
    - `calculate_face`;
    - `calculate_row`;
  - `normals`;
    - `get_normals`.

### Changed
- Removed initialization of `C` module from `MFM`.

## [0.3.3] - 2016-08-17
### Deprecated
- `Face`
  - `set_triangles` useless because `View` has triangles.
- `View`
  - `normals` useless with shaders;
  - `vertices` useless with shaders;
  - `colors` useless with shaders.

## [0.3.2] - 2016-08-17
### Changed
- Refactored the project.

## [0.3.1] - 2016-08-16
### Fixed
- `get_face` of `MFM` tried to use undefined variable.

## [0.3.0] - 2016-08-16
### Changed
- Using texture to store principal components.
- Calculating model shape via shaders.
- Calculating shadows via shaders.

### Fixed
- Flat shading model should contain only one color for entire triangle.

### Removed
- `Face`
  - `get_coefficients` in favor of `coefficients` property;
  - `get_triangles` useless because `View` has triangles;
  - `get_directed_light` in favor of `directed_light`;
  - `get_constant_light` in favor of `ambient_light`;
  - `set_light` in favor of `directed_light` and `ambient_light`.
  - `get_original_vertices` useless with shaders;
  - `get_vertices` useless with shaders;
  - `get_vertices_c` useless with shaders;
  - `get_triangles_c` useless with shaders;
  - `normal_min` useless with shaders;
  - `normal_max` useless with shaders;
  - `get_light_map_c` useless with shaders;
  - `get_normal_map_c` useless with shaders;
  - `get_normal_map` useless with shaders;
  - `get_normals` useless with shaders;
  - `get_light_map` useless with shaders;
  - `normal_map_to_normal_vectors` useless with shaders;
  - `normalize` useless with shaders.
- `Model`
  - `request_normals` in favor of `request_image`;
  - `calculate` useless with shaders;
  - `toggle_texture` useless with shaders.
- `MFM`
  - `change_coefficient` useless with shaders.

### Changed
- `get_face` method of `MFM` only allows to generate new coefficients
    &mdash; not vertices.
- `get_face` method of `MFM` should not have redundant `coefficients_only`
    argument.
- `View` allows to provide only initial `Face`, not array of coefficients.
- `ModelFitter` allows to provide only initial `Face`,
    not array of coefficients.
- `NelderMeadFitter` allows to provide only initial `Face`,
    not array of coefficients.
- `BGDFitter` allows to provide only initial `Face`,
    not array of coefficients.

## [0.2.6] - 2016-08-15
### Added
- `setup.cfg` file.

### Fixed
- `BruteForceFitter` used undefined variable.

## [0.2.5] - 2016-08-11
### Added
- `from_array` static method of `Face` to generate new face from array.

### Changed
- `BGDFitter`, `NelderMeadFitter`, `BruteForceFitter`
  - using Face instead of coefficients;
  - requesting images instead of normals;
  - fitting for light.
- `BruteForceFitter`
  - displays result of optimization in the end;
  - `offsets` constructor parameter sets initial value of parameters fitting;
  - `scales` constructor parameter controls range for parameters fitting.
- `View`
  - Using single buffer for rendering.

### Fixed
- `get_image_deviation` should work not only for `RGBA` images
    but `RA`, `RGA` as well.
- `BruteForceFitter` initial parameters should be equal to starting values,
    not zeros.
- `get_face` method of `MFM` should generate correct light conditions
    for face to be visible.

## [0.2.4] - 2016-08-08
### Added
- `bind_uniform_vector` method to `ShadersHelper`.
- `generate_face` method to `Model`.
- `face` property (getter and setter) to `Model`.

### Changed
- Using `Face` in `Model` to draw face.
- `change_light` method of `Model` restored.
- `get_image_deviation` allows to not provide normals &mdash;
    using alpha channel of provided image instead.

### Fixed
- `bind_float_texture` now accepts any iterable `size`.
- Light direction in MFM Face generation.
- `request_image` in `Model` should request image instead of normal map.
- `request_face` method in `ModelFitter` should call `request_image` of `Model`.
- `get_image` should get image from front buffer instead of back buffer
    in `View` to avoid blank data array.

## [0.2.3] - 2016-08-06
### Added
- `ModelFitter`
  - `request_face` to request render of provided Face;
  - `receive_image` to receive rendered image;
  - `initial_face` parameter to constructor
    instead of array of coefficients `initial`.
- `Model`
  - `request_image` method for requesting rendered face by Face instance.
- `ShadersHelper`
  - `bind_uniform_floats` method for binding uniform array of `float`;
  - `bind_float_texture` method for binding texture containing `float` cells.
- `Face`
  - `coefficients` property.
- `View`
  - `face` property;
  - Ability to draw face when it's set.

### Changed
- Moved `ShadersHelper` to `src` directory.

### Deprecated
- `ModelFitter`
  - `request_normals` deprecated in favor of `request_face`;
  - `receive_normals` deprecated in favor of `receive_image`;
  - `estimate_light` will be useless with new shadows model (shadows map);
  - `initial` parameter of constructor deprecated in favor of `initial_face`.
- `Model`
  - `request_normals` deprecated in favor of `request_image`;
  - `calculate` deprecated because calculations will be made by shaders;
  - `change_light` deprecated because calculations will be made by shaders.
- `Face`
  - `get_coefficients` deprecated in favor of `coefficients` property;
  - `normal_min` will be useless with new shadows model (shadows map);
  - `normal_max` will be useless with new shadows model (shadows map).
- `View`
  - Ability to draw without entire face provided.

### Fixed
- Shaders Helper with one buffer works;
- Added `shaders` folder to packages in `setup.py`.

## [0.2.2] - 2016-08-04
### Added
- Ability to set following static fields to `View`
  - `set_principal_components` setter for principal components;
  - `set_deviations` setter for deviations of principal components;
  - `set_mean_face` setter for average face.

### Changed
- `get_face` method has `coefficients_only` parameter to set
    whether it's needed to calculate the face.
- Assertion in `ShadersHelper` if uniform matrix binding failed.
- Setting PC, EV and mean face in View on MFM initialization.

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
  - `light`.
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
  least squares method.
- Face
  - `get_vertices_c` not needed;
  - `get_directed_light` has shortcut property `directed_light`;
  - `get_constant_light` has shortcut property `ambient_light`;
  - `get_light_map` not needed;
  - `get_light_map_c` not needed;
  - `get_normal_map_c` not needed;
  - `get_normal_map` not needed;
  - `set_light` has shortcut properties `directed_light` and `ambient_light`.
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

[Unreleased]: https://github.com/char-lie/mfm/compare/v0.7.2...HEAD
[0.7.2]: https://github.com/char-lie/mfm/compare/v0.7.1...v0.7.2
[0.7.1]: https://github.com/char-lie/mfm/compare/v0.7.0...v0.7.1
[0.7.0]: https://github.com/char-lie/mfm/compare/v0.6.0...v0.7.0
[0.6.0]: https://github.com/char-lie/mfm/compare/v0.5.5...v0.6.0
[0.5.5]: https://github.com/char-lie/mfm/compare/v0.5.4...v0.5.5
[0.5.4]: https://github.com/char-lie/mfm/compare/v0.5.3...v0.5.4
[0.5.3]: https://github.com/char-lie/mfm/compare/v0.5.2...v0.5.3
[0.5.2]: https://github.com/char-lie/mfm/compare/v0.5.1...v0.5.2
[0.5.1]: https://github.com/char-lie/mfm/compare/v0.5.0...v0.5.1
[0.5.0]: https://github.com/char-lie/mfm/compare/v0.4.12...v0.5.0
[0.4.12]: https://github.com/char-lie/mfm/compare/v0.4.11...v0.4.12
[0.4.11]: https://github.com/char-lie/mfm/compare/v0.4.10...v0.4.11
[0.4.10]: https://github.com/char-lie/mfm/compare/v0.4.9...v0.4.10
[0.4.9]: https://github.com/char-lie/mfm/compare/v0.4.8...v0.4.9
[0.4.8]: https://github.com/char-lie/mfm/compare/v0.4.7...v0.4.8
[0.4.7]: https://github.com/char-lie/mfm/compare/v0.4.6...v0.4.7
[0.4.6]: https://github.com/char-lie/mfm/compare/v0.4.5...v0.4.6
[0.4.5]: https://github.com/char-lie/mfm/compare/v0.4.4...v0.4.5
[0.4.4]: https://github.com/char-lie/mfm/compare/v0.4.3...v0.4.4
[0.4.3]: https://github.com/char-lie/mfm/compare/v0.4.2...v0.4.3
[0.4.2]: https://github.com/char-lie/mfm/compare/v0.4.1...v0.4.2
[0.4.1]: https://github.com/char-lie/mfm/compare/v0.4.0...v0.4.1
[0.4.0]: https://github.com/char-lie/mfm/compare/v0.3.3...v0.4.0
[0.3.3]: https://github.com/char-lie/mfm/compare/v0.3.2...v0.3.3
[0.3.2]: https://github.com/char-lie/mfm/compare/v0.3.1...v0.3.2
[0.3.1]: https://github.com/char-lie/mfm/compare/v0.3.0...v0.3.1
[0.3.0]: https://github.com/char-lie/mfm/compare/v0.2.6...v0.3.0
[0.2.6]: https://github.com/char-lie/mfm/compare/v0.2.5...v0.2.6
[0.2.5]: https://github.com/char-lie/mfm/compare/v0.2.4...v0.2.5
[0.2.4]: https://github.com/char-lie/mfm/compare/v0.2.3...v0.2.4
[0.2.3]: https://github.com/char-lie/mfm/compare/v0.2.2...v0.2.3
[0.2.2]: https://github.com/char-lie/mfm/compare/v0.2.1...v0.2.2
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
