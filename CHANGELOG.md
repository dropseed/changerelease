# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

Nothing right now.

## [1.5.0] - 2021-11-24

- Use composite action instead of docker
- Add CLS client for basic analytics
- Update pandoc example

## [1.4.0] - 2021-06-29

Simpler regular expression to accept more changelog styles and conversions from a different syntax (ex. reStructuredText).

## [1.3.0] - 2020-09-07

- Added automatic pre-release detection
- Added a `--limit` option to only sync recent versions by default in a GitHub Action
- Added a `--remote-changelog` option so you don't have to have the CHANGELOG file (or cloned repo) to use changerelease

## [1.2.0] - 2020-09-06

- Allows changelog content for a version to be empty, while still creating a GitHub Release for the tag.
- Prints parsed version changelogs
- Fail if a git tag does not exist for a version

## [1.1.1] - 2020-09-06

Added a `--no-tag-prefix` option to fix an empty issue with `--tag-prefix`.

## [1.1.0] - 2020-09-06

Adds a `tag_prefix` option so that tags don't have to start with a "v". You can now use this with tags like "1.0.0" in addition to "v1.0.0".

## [1.0.0] - 2020-09-05

The first release! Includes the `sync` command which will sync your `CHANGELOG.md` to GitHub Release notes.

[Unreleased]: https://github.com/dropseed/changerelease/compare/v1.5.0...HEAD
[1.5.0]: https://github.com/dropseed/changerelease/compare/v1.4.0...v1.5.0
[1.4.0]: https://github.com/dropseed/changerelease/compare/v1.3.0...v1.4.0
[1.3.0]: https://github.com/dropseed/changerelease/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/dropseed/changerelease/compare/v1.1.1...v1.2.0
[1.1.1]: https://github.com/dropseed/changerelease/compare/v1.1.0...v1.1.1
[1.1.0]: https://github.com/dropseed/changerelease/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/dropseed/changerelease/releases/tag/v1.0.0
