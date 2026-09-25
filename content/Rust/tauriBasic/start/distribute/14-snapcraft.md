+++
title = "14 Snapcraft"
date = 2026-09-25T21:31:08+08:00
weight = 14
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/distribute/snapcraft/](https://tauri.app/distribute/snapcraft/)

## 前置条件

**1. 安装 `snap`**

**发行版**

{{< tabpane text=true persist=disabled >}}

{{% tab header="Debian" %}}

```shell
sudo apt install snapd
```

{{% /tab %}}

{{% tab header="Arch" %}}

```shell
sudo pacman -S --needed git base-devel
git clone https://aur.archlinux.org/snapd.git
cd snapd
makepkg -si
sudo systemctl enable --now snapd.socket
sudo systemctl start snapd.socket
sudo systemctl enable --now snapd.apparmor.service
```

{{% /tab %}}

{{% tab header="Fedora" %}}

```shell
sudo dnf install snapd
# 启用 classic snap 支持
sudo ln -s /var/lib/snapd/snap /snap
```

之后重启系统。

{{% /tab %}}

{{< /tabpane >}}

**2. 安装基础 snap**

```shell
sudo snap install core22
```

**3. 安装 `snapcraft`**

```shell
sudo snap install snapcraft --classic
```

## 配置

1. 创建一个 UbuntuOne 账号。
2. 前往 [Snapcraft](https://snapcraft.io) 网站并注册一个应用名称。
3. 在项目根目录创建 snapcraft.yaml 文件。
4. 调整 snapcraft.yaml 文件中的名称。

```yaml
name: appname
base: core22
version: '0.1.0'
summary: Your summary # 79 字符以内的摘要
description: |
  Your description

grade: stable
confinement: strict

layout:
  /usr/lib/$SNAPCRAFT_ARCH_TRIPLET/webkit2gtk-4.1:
    bind: $SNAP/usr/lib/$SNAPCRAFT_ARCH_TRIPLET/webkit2gtk-4.1

apps:
  appname:
    command: usr/bin/appname
    desktop: usr/share/applications/appname.desktop
    extensions: [gnome]
    #plugs:
    #  - network
    # 在这里添加你需要的 plug，更多信息见 https://snapcraft.io/docs/snapcraft-interfaces 。
    # gnome 扩展已经包含 [ desktop, desktop-legacy, gsettings, opengl, wayland, x11, mount-observe, calendar-service ]
    #  - single-instance-plug # 如果你使用 single-instance 插件，请添加它
    #slots:
    # 添加你需要暴露给其它 snap 的 slot
    #  - single-instance-plug # 如果你使用 single-instance 插件，请添加它

# 仅当你使用 single-instance 插件时才添加这些行
# 详见 https://v2.tauri.app/plugin/single-instance/
#slots:
#  single-instance:
#    interface: dbus
#    bus: session
#    name: org.net_mydomain_MyApp.SingleInstance # 记得把 net_mydomain_MyApp 换成你的应用 ID，用 "_" 代替 "." 和 "-"
#
#plugs:
#  single-instance-plug:
#    interface: dbus
#    bus: session
#    name: org.net_mydomain_MyApp.SingleInstance # 记得把 net_mydomain_MyApp 换成你的应用 ID，用 "_" 代替 "." 和 "-"

package-repositories:
  - type: apt
    components: [main]
    suites: [noble]
    key-id: 78E1918602959B9C59103100F1831DDAFC42E99D
    url: http://ppa.launchpad.net/snappy-dev/snapcraft-daily/ubuntu

parts:
  build-app:
    plugin: dump
    build-snaps:
      - node/20/stable
      - rustup/latest/stable
    build-packages:
      - libwebkit2gtk-4.1-dev
      - build-essential
      - curl
      - wget
      - file
      - libxdo-dev
      - libssl-dev
      - libayatana-appindicator3-dev
      - librsvg2-dev
      - dpkg
    stage-packages:
      - libwebkit2gtk-4.1-0
      - libayatana-appindicator3-1
    source: .
    override-build: |
      set -eu
      npm install
      npm run tauri build -- --bundles deb
      dpkg -x src-tauri/target/release/bundle/deb/*.deb $SNAPCRAFT_PART_INSTALL/
      sed -i -e "s|Icon=appname|Icon=/usr/share/icons/hicolor/32x32/apps/appname.png|g" $SNAPCRAFT_PART_INSTALL/usr/share/applications/appname.desktop
```

### 说明

- `name` 变量定义应用的名称，必须设置为你之前注册的名称。
- `base` 变量定义你使用的 core。
- `version` 变量定义版本，每次源代码仓库变更时都应更新。
- `apps` 部分让你暴露桌面文件和二进制文件，以便用户运行你的应用。
- `package-repositories` 部分让你添加软件包仓库以帮助满足依赖。
- `build-packages`/`build-snaps` 定义 snap 的构建依赖。
- `stage-packages`/`stage-snaps` 定义 snap 的运行时依赖。
- `override-build` 部分在拉取源码之后运行一系列命令。

## 构建

```sh
sudo snapcraft
```

## 测试

```shell
snap run your-app
```

## 手动发布

```shell
snapcraft login # 使用你的 UbuntuOne 凭据登录
snapcraft upload --release=stable mysnap_latest_amd64.snap
```

## 自动构建

1. 在你应用的开发者页面上点击 `builds` 标签页。
2. 点击 `login with github`。
3. 输入你仓库的相关信息。
