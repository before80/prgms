+++
title = "9 应用图标"
date = 2026-09-25T21:31:08+08:00
weight = 9
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/develop/icons/](https://tauri.app/develop/icons/)

Tauri 自带一套基于其 logo 的默认图标集。发布应用时这并不是你想要的。为解决这个常见问题，Tauri 提供了 `icon` 命令：它以某个输入文件（默认是 `"./app-icon.png"`）为基础，生成各平台所需的所有图标。

{{% alert title="关于文件类型的说明" %}}

- `icon.icns` = macOS
- `icon.ico` = Windows
- `*.png` = Linux
- `Square*Logo.png` 和 `StoreLogo.png` = 目前未使用，但用于 AppX/MS Store 目标。

某些图标类型也可能用于上面未列出的平台（尤其是 `png`）。因此我们建议包含所有图标，即使你只打算为部分平台构建。

{{% /alert %}}

## 命令用法

**包管理器**

{{< tabpane text=true persist=disabled >}}
{{% tab header="npm" %}}

```sh
npm run tauri icon
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn tauri icon
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm tauri icon
```

{{% /tab %}}

{{% tab header="cargo" %}}

```sh
cargo tauri icon
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno task tauri icon
```

{{% /tab %}}

{{< /tabpane >}}
```console

Generate various icons for all major platforms

Usage: pnpm run tauri icon [OPTIONS] [INPUT]

Arguments:
  [INPUT]  Path to the source icon (squared PNG or SVG file with transparency) [default: ./app-icon.png]

Options:
  -o, --output <OUTPUT>        Output directory. Default: 'icons' directory next to the tauri.conf.json file
  -v, --verbose...             Enables verbose logging
  -p, --png <PNG>              Custom PNG icon sizes to generate. When set, the default icons are not generated
      --ios-color <IOS_COLOR>  The background color of the iOS icon - string as defined in the W3C's CSS Color Module Level 4 <https://www.w3.org/TR/css-color-4/> [default: #fff]
  -h, --help                   Print help
  -V, --version                Print version
```

**桌面端**图标默认会放在你的 `src-tauri/icons` 文件夹中，并会自动包含进你构建的应用里。如果你想从其它位置获取图标，可以修改 `tauri.conf.json` 文件中的这一部分：

```json
{
  "bundle": {
    "icon": [
      "icons/32x32.png",
      "icons/128x128.png",
      "icons/128x128@2x.png",
      "icons/icon.icns",
      "icons/icon.ico"
    ]
  }
}
```

**移动端**图标会直接放进 Xcode 和 Android Studio 项目中！

## 手动创建图标

如果你更愿意自己构建这些图标——例如你想为小尺寸设计更简洁的样式，或者不想依赖 CLI 内部的图像缩放——你必须确保图标满足一些要求：

- `icon.icns`：[`icns`](https://en.wikipedia.org/wiki/Apple_Icon_Image_format) 文件所需的图层尺寸与名称在 [Tauri 仓库中有说明](https://github.com/tauri-apps/tauri/blob/1.x/tooling/cli/src/helpers/icns.json)
- `icon.ico`：[`ico`](https://en.wikipedia.org/wiki/ICO_(file_format)) 文件必须包含 16、24、32、48、64 和 256 像素的图层。为了让 ICO 图像_在开发时_有最佳显示效果，32px 图层应当是第一个图层。
- `png`：png 图标的要求是：宽 == 高、RGBA（RGB + 透明度）、每像素 32 位（每通道 8 位）。桌面上常见的期望尺寸是 32、128、256 和 512 像素。我们建议至少与 `tauri icon` 的输出保持一致：`32x32.png`、`128x128.png`、`128x128@2x.png` 和 `icon.png`。

### Android

在 Android 上你需要满足同样要求但尺寸不同的 png 图标。它们也需要直接放进 Android Studio 项目：

- `src-tauri/gen/android/app/src/main/res/`
  - `mipmap-hdpi/`
    - `ic_launcher.png` 和 `ic_launcher_round.png`：49x49px
    - `ic_launcher_foreground.png`：162x162px
  - `mipmap-mdpi/`
    - `ic_launcher.png` 和 `ic_launcher_round.png`：48x48px
    - `ic_launcher_foreground.png`：108x108px
  - `mipmap-xhdpi/`
    - `ic_launcher.png` 和 `ic_launcher_round.png`：96x96px
    - `ic_launcher_foreground.png`：216x216px
  - `mipmap-xxhdpi/`
    - `ic_launcher.png` 和 `ic_launcher_round.png`：144x144px
    - `ic_launcher_foreground.png`：324x324px
  - `mipmap-xxxhdpi/`
    - `ic_launcher.png` 和 `ic_launcher_round.png`：192x192px
    - `ic_launcher_foreground.png`：432x432px

如果无法使用 `tauri icon`，我们建议改用 Android Studio 的 [Image Asset Studio](https://developer.android.com/studio/write/create-app-icons)。

### iOS

在 iOS 上你需要满足同样要求但**不带透明度**、尺寸不同的 png 图标。它们也需要直接放进 Xcode 项目的 `src-tauri/gen/apple/Assets.xcassets/AppIcon.appiconset/` 中。需要以下图标：

- 20px 的 1x、2x、3x，外加一个额外图标
- 29px 的 1x、2x、3x，外加一个额外图标
- 40px 的 1x、2x、3x，外加一个额外图标
- 60px 的 2x、3x
- 76px 的 1x、2x
- 83.5px 的 2x
- 512px 的 2x，保存为 `AppIcon-512@2x.png`

文件名格式为 `AppIcon-{size}x{size}@{scaling}{extra}.png`。对 20px 图标来说，这意味着你需要 20x20、40x40 和 60x60 三种尺寸，分别命名为 `AppIcon-20x20@1x.png`、`AppIcon-20x20@2x.png`、`AppIcon-20x20@3x.png`，并且 `2x` 还要额外保存为 `AppIcon-20x20@2x-1.png`（即“额外图标”）。
