# Change Log
All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/).

## [Unreleased]
### Changed
- Refactored CHANGELOG.

### Removed
- Removed redundant `Image` class.

## [0.1.0] - 2016-04-21
### Added
- CHANGELOG.
- [travis-ci](https://travis-ci.org/char-lie/patterns_recognition).
- [coveralls](https://coveralls.io/github/char-lie/patterns_recognition?branch=master).
- Method for removal of not connected vertices and edges from Graph.
- New Semiring (max, +) on R &mdash; to find length of maximal path.
- Perceptron solver class to separate two linearly separable sets of points.
- Examples for Perceptron setup demonstration, in which points are separated by
  - Circle;
  - Points with circles around them of same class as corresponding points;
  - Ellipse with focuses parallel to axis with center in random position;
  - Ellipse with random focuses with center in origin;
  - Quadratic form;
  - Cubic curve;
  - Random order curve, random parameters;
  - Random order curve, dots picked by user in real-time.

### Changed
- Moved preparation method from Dynamic Programming solver
    to general Graph class.
- Removed redundant trailing spaces in code.

## [0.0.3] - 2016-01-07
### Added
- Dynamic Programming as a separate Solver class.
- Graph class to solve graph-based problems.
- Semiring class and several child classes.
    to perform operations on different semirings:
  - (argmin, +) on R &mdash; to gather arguments of minimal path;
  - (min, +) on R &mdash; to find length of minimal path;
  - (min, +) on R<sup>2</sup> &mdash; to find length of minimal path;
      represented by two numbers;
  - (+, ×) on R &mdash; to find probability of all paths.
- Image class for images processing.
- Matrix Pointer class for lower memory and time cost images processing.
- Covered each class by **unit tests**.

### Changed
- Rewritten letters string recognition example using new classes.

## [0.0.2] - 2015-09-22
### Fixed
- Increased speed of basic example with letters string recognition.

## 0.0.1 - 2015-09-22
### Added
- Added basic example with letters string recognition.

[Unreleased]: https://github.com/char-lie/patterns_recognition/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/char-lie/patterns_recognition/compare/v0.0.3...v0.1.0
[0.0.3]: https://github.com/char-lie/patterns_recognition/compare/v0.0.2...v0.0.3
[0.0.2]: https://github.com/char-lie/patterns_recognition/compare/v0.0.1...v0.0.2
