+++
title = "7 Flathub"
date = 2026-09-25T21:31:08+08:00
weight = 7
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/distribute/flatpak/](https://tauri.app/distribute/flatpak/)

**发行类型**

{{< tabpane text=true persist=disabled >}}

{{% tab header="开源" %}}

1. 获取所需工具。

```sh
git submodule add https://github.com/flatpak/flatpak-builder-tools.git
cd flatpak-builder-tools/node/flatpak_node_generator
pipx install . # 改成你偏好的安装方式
```

2. 生成你的 source 文件

**包管理器**

{{< tabpane text=true persist=disabled >}}

{{% tab header="Yarn" %}}

```sh
# 生成 Node sources
flatpak-node-generator --no-requests-cache -o node-sources.json yarn /path/to/your/lock/file/yarn.lock

# 生成 cargo sources

python3 flatpak-builder-tools/cargo/flatpak-cargo-generator.py -o cargo-sources.json src-tauri/Cargo.lock
```

{{% /tab %}}

{{% tab header="NPM" %}}

```sh
# 生成 Node sources
flatpak-node-generator --no-requests-cache -o node-sources.json npm /path/to/your/lock/file/package-lock.json

# 生成 cargo sources
python3 flatpak-builder-tools/cargo/flatpak-cargo-generator.py -o cargo-sources.json src-tauri/Cargo.lock
```

{{% /tab %}}

{{< /tabpane >}}

3. 创建你的 metainfo
   请务必替换相关字段。

```xml
<?xml version="1.0" encoding="UTF-8"?>
<component type="desktop-application">
    <id>org.your.id</id>
    <launchable type="desktop-id">org.your.id.desktop</launchable>
    <name>Your Apps Name</name>
    <developer id="io.github.roseblume.rosemusic">
        <name>Your Name</name>
    </developer>
    <content_rating type="oars-1.1">
    </content_rating>
    <keywords>
        <keyword>Keyword1</keyword>
        <keyword>Keyword2</keyword>
    </keywords>
    <branding>
        <color type="primary" scheme_preference="light">#00ffff</color>
        <color type="primary" scheme_preference="dark">#0c9aff</color>
    </branding>
    <recommends>
        <display_length compare="ge">360</display_length>
    </recommends>
    <summary>Your Summary</summary>

    <metadata_license>MIT</metadata_license>
    <project_license>MIT</project_license>
    <url type="homepage">https://github.com/Your-Username/Your-Repo</url>

    <supports>
        <control>pointing</control>
        <control>keyboard</control>
        <control>touch</control>
    </supports>

    <description>
        <p>
            Your Description
        </p>
    </description>
    <screenshots>
        <screenshot type="default">
            <image>https://site.com/your-image.png</image>
            <caption>Your Caption</caption>
        </screenshot>
    </screenshots>
    <releases>
        <release version="1.0.0" date="2024-11-02" >
            <description>
            <ul>
                <li>Updated UI</li>
                <li>Added Electronic Genre</li>
            </ul>
            </description>
        </release>
    </releases>
    <update_contact>your-email@place.com</update_contact>

</component>
```

建议把该元数据包含进你的 debian 打包产物中，虽然并非必需。这可以通过调整打包配置实现，如下所示。

```json
"linux": {
      "deb": {
        "files": {
          "/usr/share/metainfo/org.your.id.metainfo.xml": "relative/path/from/your/tauri.conf.json/to/your/org.your.id.metainfo.xml"
        }
      }
    }
```

4. 创建你的 manifest

```yaml
id: org.your.id

runtime: org.gnome.Platform
runtime-version: '47'
sdk: org.gnome.Sdk

command: tauri-app
finish-args:

- --socket=wayland # 显示窗口所需权限
- --socket=fallback-x11 # 在传统窗口系统上显示窗口所需权限
- --device=dri # OpenGL，并非所有项目都需要
- --share=ipc
  sdk-extensions:
- org.freedesktop.Sdk.Extension.node20
- org.freedesktop.Sdk.Extension.rust-stable
  build-options:
  append-path: /usr/lib/sdk/node20/bin:/usr/lib/sdk/rust-stable/bin

modules:

- name: your-command
  buildsystem: simple
  env:
  HOME: /run/build/your-module
  CARGO_HOME: /run/build/your-module/src-tauri
  XDG_CACHE_HOME: /run/build/your-module/flatpak-node/cache
  yarn_config_offline: 'true'
  yarn_config_cache: /run/build/your-module/flatpak-node/yarn-cache
  sources:
  - type: git
    url: https://github.com/Your-Github-Username/Your-Git-Repo.git
    tag: v1.2.2
  - cargo-sources.json
  - node-sources.json
    build-commands:
  - echo -e 'yarn-offline-mirror "/run/build/your-module/flatpak-node/yarn-mirror"\nyarn-offline-mirror-pruning true' > /run/build/your-module/.yarnrc
  - mkdir -p src-tauri/.cargo && echo -e '[source.crates-io]\nreplace-with = "vendored-sources"\n\n[source.vendored-sources]\ndirectory = "/run/build/your-module/cargo/vendor"' > src-tauri/.cargo/config.toml
  - yarn install --offline --immutable --immutable-cache --inline-builds
  - yarn run tauri build -- -b deb
  - ar -x src-tauri/target/release/bundle/deb/\*.deb
  - tar -xf src-tauri/target/release/bundle/deb/your-app/data.tar.gz
  - install -Dm755 src-tauri/target/release/bundle/deb/your-app/data/usr/bin/your-command /app/bin/your-command
  - install -Dm644 src-tauri/target/release/bundle/deb/your-app/data/usr/share/applications/your-app.desktop /app/share/applications/org.your.id.desktop
  - install -Dm644 src-tauri/target/release/bundle/deb/your-app/data/usr/share/icons/hicolor/128x128/apps/your-app.png /app/share/icons/hicolor/128x128/apps/your-app.png
  - install -Dm644 src-tauri/target/release/bundle/deb/your-app/data/usr/share/icons/hicolor/32x32/apps/your-app.png /app/share/icons/hicolor/32x32/apps/your-app.png
  - install -Dm644 src-tauri/target/release/bundle/deb/your-app/data/usr/share/icons/hicolor/256x256@2/apps/your-app.png /app/share/icons/hicolor/512x512/apps/your-app.png
  - install -Dm644 src-tauri/target/release/bundle/deb/your-app/data/usr/share/icons/hicolor/scalable/apps/your-app.svg /app/share/icons/hicolor/scalable/apps/your-app.svg

  - install -Dm644 src-tauri/target/release/bundle/deb/your-app/data/usr/share/metainfo/org.your.id /app/share/metainfo/org.your.id

```

## 提交到 Flathub

**_1. Fork [Flathub 仓库](https://github.com/flathub/flathub/fork)_**

**_2. 克隆你的 fork_**

```shell
git clone --branch=new-pr git@github.com:your_github_username/flathub.git
```

**_3. 进入该仓库_**

```shell
cd flathub
```

**_4. 创建一个新分支_**

```shell
git checkout -b your_app_name
```

**_5. 在 GitHub 上针对 `new-pr` 分支发起 pull request_**

**_6. 你的应用现在会进入审核流程，期间可能会被要求对项目做修改。_**

{{% /tab %}}

{{% tab header="闭源" %}}

关于 Flatpak 工作原理的详细信息，你可以阅读[构建你的第一个 Flatpak](https://docs.flatpak.org/en/latest/first-build.html)。

本指南假设你想通过 [Flathub](https://flathub.org/)（最常用的 Flatpak 分发平台）分发你的 Flatpak。如果你打算使用其它平台，请查阅它们的文档。

## 前置条件

要在 Flatpak 运行时中测试应用，你可以先在本地构建 Flatpak，再上传到 Flathub。如果你想快速分享开发构建，这同样有用。

**1. 安装 `flatpak` 与 `flatpak-builder`**

要在本地构建 Flatpak，你需要 `flatpak` 和 `flatpak-builder` 工具。例如在 Ubuntu 上可以运行：

**发行版**

{{< tabpane text=true persist=disabled >}}

{{% tab header="Debian" %}}

```sh
sudo apt install flatpak flatpak-builder
```

{{% /tab %}}

{{% tab header="Arch" %}}

```sh
sudo pacman -S --needed flatpak flatpak-builder
```

{{% /tab %}}

{{% tab header="Fedora" %}}

```sh
sudo dnf install flatpak flatpak-builder
```

{{% /tab %}}

{{% tab header="Gentoo" %}}

```sh
sudo emerge --ask \
sys-apps/flatpak \
dev-util/flatpak-builder
```

{{% /tab %}}

{{< /tabpane >}}

**2. 安装 Flatpak 运行时**

```shell
flatpak install flathub org.gnome.Platform//46 org.gnome.Sdk//46
```

**3. [构建你的 tauri 应用的 .deb 包](https://tauri.app/reference/config/#bundleconfig)**

**4. [创建一个 AppStream MetaInfo 文件](https://www.freedesktop.org/software/appstream/metainfocreator/#/guiapp)**

**5. 创建 flatpak manifest**

```yaml
# flatpak-builder.yaml
id: <identifier>

runtime: org.gnome.Platform
runtime-version: '47'
sdk: org.gnome.Sdk

command: <main_binary_name>
finish-args:
  - --socket=wayland # 显示窗口所需权限
  - --socket=fallback-x11 # 显示窗口所需权限
  - --device=dri # OpenGL，并非所有项目都需要
  - --share=ipc
  - --talk-name=org.kde.StatusNotifierWatcher # 可选：仅当你的应用使用托盘图标时需要
  - --filesystem=xdg-run/tray-icon:create # 可选：仅当你的应用使用托盘图标时需要——见下面的替代做法
  # - --env=WEBKIT_DISABLE_COMPOSITING_MODE=1 # 可选：可能解决 Wayland 上 webview 黑屏的某些问题

modules:
  - name: binary
    buildsystem: simple

    sources:
      # 对之前生成的 flatpak metainfo 文件的引用
      - type: file
        path: flatpak.metainfo.xml
      # 如果你使用 GitHub releases，可以指向一个已有的远程文件
      - type: file
        url: https://github.com/your_username/your_repository/releases/download/v1.0.1/yourapp_1.0.1_amd64.deb
        sha256: 08305b5521e2cf0622e084f2b8f7f31f8a989fc7f407a7050fa3649facd61469 # 使用远程 source 时这是必需的
        only-arches: [x86_64] # 该 source 只在 x86_64 电脑上使用
      # 你也可以使用本地文件进行测试
      # - type: file
      #   path: yourapp_1.0.1_amd64.deb
    build-commands:
      - set -e

      # 解压 deb 包
      - mkdir deb-extract
      - ar -x *.deb --output deb-extract
      - tar -C deb-extract -xf deb-extract/data.tar.gz

      # 复制二进制文件
      - 'install -Dm755 deb-extract/usr/bin/<executable_name> /app/bin/<executable_name>'

      # 如果你打包了额外的资源文件，也应当复制它们：
      - mkdir -p /app/lib/<product_name>
      - cp -r deb-extract/usr/lib/<product_name>/. /app/lib/<product_name>
      - find /app/lib/<product_name> -type f -exec chmod 644 {} \;

      # 复制 desktop 文件并确保设置了正确的图标
      - sed -i 's/^Icon=.*/Icon=<identifier>/' deb-extract/usr/share/applications/<product_name>.desktop
      - install -Dm644 deb-extract/usr/share/applications/<product_name>.desktop /app/share/applications/<identifier>.desktop

      # 复制图标
      - install -Dm644 deb-extract/usr/share/icons/hicolor/128x128/apps/<main_binary_name>.png /app/share/icons/hicolor/128x128/apps/<identifier>.png
      - install -Dm644 deb-extract/usr/share/icons/hicolor/32x32/apps/<main_binary_name>.png /app/share/icons/hicolor/32x32/apps/<identifier>.png
      - install -Dm644 deb-extract/usr/share/icons/hicolor/256x256@2/apps/<main_binary_name>.png /app/share/icons/hicolor/256x256@2/apps/<identifier>.png
      - install -Dm644 flatpak.metainfo.xml /app/share/metainfo/<identifier>.metainfo.xml
```

Gnome 46 运行时包含了标准 Tauri 应用的全部依赖及其正确版本。

{{% alert title="不修改 Flatpak manifest 就使用 tray-icon" %}}
如果你不想让应用访问 $XDG_RUNTIME_DIR（tray-icon 在 linux 上保存的位置），你可以修改 tauri 保存托盘图片的路径：

```rust
TrayIconBuilder::new()
  .icon(app.default_window_icon().unwrap().clone())
  .temp_dir_path(app.path().app_cache_dir().unwrap()) // 会保存到应用已有权限的缓存文件夹（$XDG_CACHE_HOME）
  .build()
  .unwrap();
```

{{% /alert %}}

**5. 安装并测试应用**

```shell

# 安装该 flatpak
flatpak-builder --force-clean --user --disable-cache --repo flatpak-repo flatpak flatpak-builder.yaml

# 运行它
flatpak run <your flatpak id> # 或通过你的桌面环境

# 更新它
flatpak -y --user update <your flatpak id>
```

## 添加额外的库

如果你的最终二进制文件比默认 tauri 应用需要更多库，你需要在 flatpak manifest 中加入它们。
有两种做法。为了快速的本地开发，直接包含本地系统上已构建好的库文件（`.so`）也许可行。
但这不推荐用于 flatpak 的最终构建，因为你本地的库文件并不是为 flatpak 运行时环境构建的。
这可能引入各种很难排查的 bug。
因此，推荐在 flatpak 内部把程序依赖的库作为构建步骤从源码构建。

## 提交到 flathub

**_1. Fork [Flathub 仓库](https://github.com/flathub/flathub/fork)_**

**_2. 克隆你的 fork_**

```shell
git clone --branch=new-pr git@github.com:your_github_username/flathub.git
```

**_3. 进入该仓库_**

```shell
cd flathub
```

**_4. 创建一个新分支_**

```shell
git checkout -b your_app_name
```

**_5. 把你应用的 manifest 加入该分支。提交你的改动，然后推送它们。_**

**_6. 在 GitHub 上针对 `new-pr` 分支发起 pull request_**

**_7. 你的应用现在会进入审核流程，期间可能会被要求对项目做修改。_**

当你的 pull request 被批准后，你会收到编辑你应用仓库的邀请。此后你就可以持续更新你的应用了。

你可以[在 flatpak 文档中](https://docs.flatpak.org/en/latest/dependencies.html#bundling)了解更多内容。

{{% /tab %}}

{{< /tabpane >}}
