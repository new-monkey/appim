# appim

[![CI](https://github.com/new-monkey/appim/actions/workflows/ci.yml/badge.svg)](https://github.com/new-monkey/appim/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)

把 AppImage 像正常桌面软件一样装进用户目录 —— 不需要 root，不需要 FUSE，也不依赖
第三方打包器。

[English](README.md) | 简体中文

## 为什么

用 AppImage 通常意味着：把一个上百 MB 的文件塞在某个角落，`chmod +x`，然后每次都
从终端启动。它不会出现在应用菜单里，没有图标，也没有可用的命令。

`appim` 解决这些问题：解包一次，读取包里自带的 `.desktop` 与图标，然后按 XDG 标准
装到当前用户目录：

```sh
appim install Cherry-Studio-1.9.12-x86_64.AppImage
```

之后应用会以正确的图标出现在启动器里，`cherry-studio` 也能在任何 shell 里直接运行。

## 要求

- Linux
- Python 3.8 或更新版本（`python3` 需在 `PATH` 中）
- 只依赖标准库，无需 `pip install`

`appim` 是一个自包含的单文件脚本。

## 安装

```sh
git clone https://github.com/new-monkey/appim.git
cd appim
make install            # 安装到 ~/.local/bin/appim
```

或者直接下载脚本：

```sh
curl -fsSL https://raw.githubusercontent.com/new-monkey/appim/main/appim \
  -o /tmp/appim && install -Dm755 /tmp/appim ~/.local/bin/appim
```

请确认 `~/.local/bin` 在 `PATH` 中 —— 不在的话 `appim` 会给出提示。

## 用法

```sh
appim install <file.AppImage>   # 安装，或升级已安装的应用
appim list                      # 列出已安装应用及其文件
appim remove <name>             # 卸载本工具创建的全部内容
appim --version
```

`remove` 接收的应用名要和 `list` 显示的一致。含空格的名字加不加引号都可以：

```sh
appim remove Cherry Studio
```

## 会写入哪些位置

以桌面文件里 `Name=` 为 `Cherry Studio` 的应用为例：

| 路径 | 用途 |
| --- | --- |
| `~/.local/share/appiminst/apps/Cherry Studio/<原始文件名>` | AppImage 副本，保持可执行 |
| `~/.local/share/applications/Cherry Studio.desktop` | 启动项，`Exec=`/`Icon=` 改写为绝对路径 |
| `~/.local/share/icons/hicolor/<尺寸>/apps/Cherry Studio.<ext>` | 从 AppImage 中提取的图标 |
| `~/.local/bin/cherry-studio` | 指向已安装 AppImage 的软链接 |

不会写入 `$HOME` 之外的任何位置，也不需要 root。

说明：

- `Exec=` 会保留原始启动项的参数（如 `--no-sandbox %U`），只改写可执行文件路径。
- 图标优先取 hicolor 主题中的 `scalable` SVG，其次按位图尺寸；`pixmaps` 和根目录
  图标作为兜底。
- 如果解包失败（部分 AppImage 不可提取），则改用文件名作为应用名、使用
  `application-x-executable` 占位图标继续安装，而不是直接失败。

## 卸载

```sh
appim remove <name>
```

卸载工具本身：`make uninstall`。

## 兼容性

适用于任何读取 XDG `.desktop` 文件与 hicolor 图标主题的桌面环境 —— GNOME、KDE
Plasma、Xfce、Cinnamon、MATE、LXQt 以及多数独立启动器。`Exec=` 指向稳定路径，因此
再次执行 `appim install` 升级后启动项依然有效。

## 开发

```sh
make test     # 标准库 unittest，无外部依赖
make lint     # ruff check + format check（pipx install ruff）
make check    # 两者都跑
```

目录结构：

```
appim                    全部实现（单文件）
tests/test_appim.py      单元测试
```

提交 PR 前请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)；版本历史见
[CHANGELOG.md](CHANGELOG.md)。

## 许可证

[MIT](LICENSE)
