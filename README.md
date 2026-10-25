# appim

[![CI](https://github.com/new-monkey/appim/actions/workflows/ci.yml/badge.svg)](https://github.com/new-monkey/appim/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)

Install AppImages into your home directory like a proper desktop application —
no root, no FUSE, no third-party packager.

English | [简体中文](README.zh-CN.md)

## Why

Running an AppImage means keeping a 100 MB file somewhere, `chmod +x`-ing it, and
launching it from a terminal every time. It never shows up in your application
menu, it has no icon, and it has no command on `PATH`.

`appim` fixes that. It unpacks the AppImage once, reads the `.desktop` entry and
icon the package already ships, then installs them into the standard XDG
locations for the current user:

```
appim install Cherry-Studio-1.9.12-x86_64.AppImage
```

After that the app appears in your launcher with the right icon, and `cherry-studio`
works from any shell.

## Requirements

- Linux
- Python 3.8 or newer (`python3` must be on `PATH`)
- Standard library only — nothing to `pip install`

`appim` is a single self-contained script.

## Install

```sh
git clone https://github.com/new-monkey/appim.git
cd appim
make install            # copies to ~/.local/bin/appim
```

Or fetch the script directly:

```sh
curl -fsSL https://raw.githubusercontent.com/new-monkey/appim/main/appim \
  -o /tmp/appim && install -Dm755 /tmp/appim ~/.local/bin/appim
```

Make sure `~/.local/bin` is on your `PATH` — `appim` prints a hint if it isn't.

## Usage

```sh
appim install <file.AppImage>   # install, or upgrade an already installed app
appim list                      # list installed apps and their binaries
appim remove <name>             # uninstall everything this tool created
appim --version
```

`remove` takes the application name exactly as `list` shows it. Names containing
spaces work with or without quotes:

```sh
appim remove Cherry Studio
```

## What gets written

For an app whose desktop `Name=` is `Cherry Studio`:

| Path | Purpose |
| --- | --- |
| `~/.local/share/appiminst/apps/Cherry Studio/<original-filename>` | the AppImage, copied and kept executable |
| `~/.local/share/applications/Cherry Studio.desktop` | launcher entry, `Exec=`/`Icon=` rewritten to absolute paths |
| `~/.local/share/icons/hicolor/<size>/apps/Cherry Studio.<ext>` | icon pulled from the AppImage |
| `~/.local/bin/cherry-studio` | symlink to the installed AppImage |

Nothing outside `$HOME` is touched, and nothing needs root.

Notes:

- `Exec=` keeps any arguments the original entry used (`--no-sandbox %U` and
  friends) and only rewrites the binary path.
- Icons are picked from the hicolor theme, preferring `scalable` SVG over bitmap
  sizes; `pixmaps` and root-level icons are fallbacks.
- If extraction fails (some AppImages are not extractable), the file name is used
  as the application name and a generic `application-x-executable` icon is used
  instead of failing the install.

## Uninstall

```sh
appim remove <name>
```

To drop the tool itself: `make uninstall`.

## Compatibility

Any desktop environment that reads XDG `.desktop` files and the hicolor icon
theme — GNOME, KDE Plasma, Xfce, Cinnamon, MATE, LXQt, and most standalone
launchers. Because `Exec=` points at a stable path, upgrades via
`appim install` keep the entry working.

The CLI output is currently in Chinese. Output localisation is tracked as a
future improvement; the interface (subcommands and flags) is English.

## Development

```sh
make test     # stdlib unittest, no dependencies
make lint     # ruff check + format check (pipx install ruff)
make check    # both
```

Layout:

```
appim                    the whole tool (single script)
tests/test_appim.py      unit tests
```

See [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request, and
[CHANGELOG.md](CHANGELOG.md) for release history.

## License

[MIT](LICENSE)
