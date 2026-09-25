+++
title = "2 AppImage"
date = 2026-09-25T21:31:08+08:00
weight = 2
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/distribute/appimage/](https://tauri.app/distribute/appimage/)

`AppImage` 是一种不依赖系统已安装软件包的分发格式，而是把应用所需的所有依赖和文件都打包进去。因此输出文件更大，但更容易分发，因为它被许多 Linux 发行版支持，且无需安装即可执行。用户只需把文件设为可执行（`chmod a+x MyProject.AppImage`），然后运行它（`./MyProject.AppImage`）。

AppImage 很方便：当你无法制作针对某个发行版包管理器的软件包时，它简化了分发流程。不过你仍应谨慎使用，因为文件体积会从 2-6 MB 增长到 70+ MB。

{{% alert title="注意" %}}

macOS 和 Linux 上的 GUI 应用不会从你的 shell dotfile（`.bashrc`、`.bash_profile`、`.zshrc` 等）继承 `$PATH`。请查看 Tauri 的 [fix-path-env-rs](https://github.com/tauri-apps/fix-path-env-rs) crate 来修复这个问题。

{{% /alert %}}

## 限制

glibc 之类的核心库经常会破坏与旧系统的兼容性。因此，你必须使用你打算支持的最旧基础系统来构建 Tauri 应用，并且该系统还要提供 Tauri v2 所需的 WebKitGTK 4.1 软件包。Ubuntu 22.04 和 Debian 12 是合适的基线示例，因为它们从标准软件仓库提供 `libwebkit2gtk-4.1-dev`。在更新的基础系统上构建可能提高应用所需的最低 glibc 版本，因此在旧系统上运行时可能遇到 `/usr/lib/libc.so.6: version 'GLIBC_2.33' not found` 这样的运行时错误。我们建议使用 Docker 容器或 GitHub Actions 为 Linux 构建你的 Tauri 应用。

更多信息请参阅 [tauri-apps/tauri#1355](https://github.com/tauri-apps/tauri/issues/1355) 和 [rust-lang/rust#57497](https://github.com/rust-lang/rust/issues/57497)，以及 [AppImage 指南](https://docs.appimage.org/reference/best-practices.html#binaries-compiled-on-old-enough-base-system)。

## 通过 GStreamer 支持多媒体

如果你的应用播放音频／视频，你需要启用 `tauri.conf.json > bundle > linux > appimage > bundleMediaFramework`。这会增大 AppImage 包的体积，以包含媒体播放所需的额外 gstreamer 文件。该标志目前只在 Ubuntu 构建系统上得到完整支持。请确保你的构建系统具备应用运行时可能需要的所有插件。

{{% alert title="警告" color="warning" %}}

`ugly` 包中的 GStreamer 插件采用的许可证可能使其难以作为应用的一部分分发。

{{% /alert %}}

## 自定义文件

要把不想通过 Tauri 的 [`resources` 特性](../../develop/6-resources/)包含的文件加入 AppImage，你可以在 `tauri.conf.json > bundle > linux > appimage > files` 中提供文件或文件夹列表。该配置对象把 AppImage 中的路径映射到文件系统上的文件路径（相对于 `tauri.conf.json` 文件）。下面是一个配置示例：

```json
{
  "bundle": {
    "linux": {
      "appimage": {
        "files": {
          "/usr/share/README.md": "../README.md", // 把 ../README.md 复制到 <appimage>/usr/share/README.md
          "/usr/assets": "../assets/" // 把整个 ../assets 目录复制到 <appimage>/usr/assets
        }
      }
    }
  }
}
```

{{% alert title="注意" %}}

注意目标路径目前必须以 `/usr/` 开头。

{{% /alert %}}

## 面向 ARM 设备的 AppImage

{{% alert title="2025 年 8 月更新" %}}
GitHub 已经[发布](https://github.blog/changelog/2025-08-07-arm64-hosted-runners-for-public-repositories-are-now-generally-available/#get-started)了公开可用的 `ubuntu-22.04-arm` 和 `ubuntu-24.04-arm` runner。你可以直接使用它们构建应用而无需任何改动，一次典型构建大约需要 10 分钟。
{{% /alert %}}

Tauri 使用的 AppImage 工具 `linuxdeploy` 目前[不支持交叉编译] ARM AppImage。这意味着 ARM AppImage 只能在 ARM 设备或模拟器上构建。

关于利用 QEMU 构建应用的示例 workflow，请参阅我们的 [GitHub Action 指南](../pipelines/2-github/#arm-runner-编译)。注意这种方式极其缓慢，只建议在构建分钟数免费的公开仓库中使用。在私有仓库中，GitHub 的 ARM runner 应该更具成本效益，也更容易配置。

[不支持交叉编译]: https://github.com/linuxdeploy/linuxdeploy/issues/258
