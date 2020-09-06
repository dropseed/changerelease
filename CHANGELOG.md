# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

Nothing right now.

## [1.2.0] - 2020-09-06

Allows changelog content for a version to be empty, while still creating a GitHub Release for the tag.

## [1.1.1] - 2020-09-06

Added a `--no-tag-prefix` option to fix an empty issue with `--tag-prefix`.

## [1.1.0] - 2020-09-06

Adds a `tag_prefix` option so that tags don't have to start with a "v". You can now use this with tags like "1.0.0" in addition to "v1.0.0".

## [1.0.0] - 2020-09-05

The first release! Includes the `sync` command which will sync your `CHANGELOG.md` to GitHub Release notes.

[Unreleased]: https://github.com/dropseed/changerelease/compare/v1.1.1...HEAD
[1.2.0]: https://github.com/dropseed/changerelease/compare/v1.1.1...v1.2.0
[1.1.1]: https://github.com/dropseed/changerelease/compare/v1.1.0...v1.1.1
[1.1.0]: https://github.com/dropseed/changerelease/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/dropseed/changerelease/releases/tag/v1.0.0
