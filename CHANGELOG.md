# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-10-25

### Added

- `appim install <file.AppImage>`: extract the AppImage's embedded `.desktop` entry
  and icon, install the binary under `~/.local/share/appiminst/apps/`, write a
  patched desktop entry to `~/.local/share/applications/`, place the icon in the
  hicolor theme, and symlink the command into `~/.local/bin/`.
- `appim remove <name>`: remove every artifact the installer created.
- `appim list`: list installed applications.
- `--version` flag.

[Unreleased]: https://github.com/new-monkey/appim/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/new-monkey/appim/releases/tag/v0.1.0
