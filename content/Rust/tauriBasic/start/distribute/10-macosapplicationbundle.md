+++
title = "10 macOS 应用程序包"
date = 2026-09-25T21:31:08+08:00
weight = 10
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/distribute/macos-application-bundle/](https://tauri.app/distribute/macos-application-bundle/)

应用程序包（application bundle）是 macOS 上执行的包格式。它就是一个简单的目录，包含应用成功运行所需的一切：
应用可执行文件、资源、Info.plist 文件以及 macOS framework 等其它文件。

要把应用打包为 macOS 应用程序包，你可以在 Mac 电脑上使用 Tauri CLI 运行 `tauri build` 命令：

**包管理器**

{{< tabpane text=true persist=disabled >}}

{{% tab header="npm" %}}

```sh
npm run tauri build -- --bundles app
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn tauri build --bundles app
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm tauri build --bundles app
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno task tauri build --bundles app
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun tauri build --bundles app
```

{{% /tab %}}

{{% tab header="cargo" %}}

```sh
cargo tauri build --bundles app
```

{{% /tab %}}

{{< /tabpane >}}

{{% alert title="注意" %}}

macOS 和 Linux 上的 GUI 应用不会从你的 shell dotfile（`.bashrc`、`.bash_profile`、`.zshrc` 等）继承 `$PATH`。请查看 Tauri 的 [fix-path-env-rs](https://github.com/tauri-apps/fix-path-env-rs) crate 来修复这个问题。

{{% /alert %}}

## 文件结构

macOS 应用程序包是一个具有以下结构的目录：

```
├── <productName>.app
│   ├── Contents
│   │   ├── Info.plist
│   │   ├── ...来自 [`tauri.conf.json > bundle > macOS > files`] 的额外文件
│   ├── MacOS
│   │   ├── <app-name>（应用可执行文件）
│   ├── Resources
│   │   ├── icon.icns（应用图标）
│   │   ├── ...来自 [`tauri.conf.json > bundle > resources`] 的资源
│   ├── _CodeSignature（Apple 生成的 codesign 信息）
│   ├── Frameworks
│   ├── PlugIns
│   ├── SharedSupport
```

更多信息请参阅[官方文档](https://developer.apple.com/library/archive/documentation/CoreFoundation/Conceptual/CFBundles/BundleTypes/BundleTypes.html)。

## 原生配置

应用程序包由 `Info.plist` 文件配置，其中包含你的应用身份等键值对，以及 macOS 读取的配置值。

Tauri 会自动配置最重要的属性，例如应用二进制文件名、版本、bundle 标识符、最低系统版本等。

要扩展该配置文件，请在 `src-tauri` 文件夹中创建 `Info.plist` 文件并加入你想要的键值对：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>NSCameraUsageDescription</key>
	<string>Request camera access for WebRTC</string>
	<key>NSMicrophoneUsageDescription</key>
	<string>Request microphone access for WebRTC</string>
</dict>
</plist>
```

这个 `Info.plist` 文件会与 Tauri CLI 生成的值合并。覆盖应用版本之类的默认值时要小心，因为它们可能与其他配置值冲突并引入意料之外的行为。

更多信息请参阅 [Info.plist 官方文档](https://developer.apple.com/documentation/bundleresources/information_property_list)。

### Info.plist 本地化

`Info.plist` 文件本身只支持单一语言，通常是英语。如果你想支持多种语言，可以为每种额外语言创建 `InfoPlist.strings` 文件。每个文件都放在应用程序包 `Resources` 目录中各自的语言特定 `lproj` 目录里。

要自动打包这些文件，你可以利用 Tauri 的 [resources](../../develop/6-resources/) 特性。为此，请在项目中按以下模式创建文件结构：

```
├── src-tauri
│   ├── tauri.conf.json
│   ├── infoplist
│   │   ├── de.lproj
│   │   │   ├── InfoPlist.strings
│   │   ├── fr.lproj
│   │   │   ├── InfoPlist.strings
```

`infoplist` 目录名可以随意取，只要你在下面的 resources 配置中相应更新即可；但 `lproj` 目录必须遵循 `<lang-code>.lproj` 命名，字符串目录文件必须命名为 `InfoPlist.strings`（小写 i、大写 P）。大多数情况下，语言代码应当是遵循 [BCP 47](https://www.rfc-editor.org/rfc/bcp/bcp47.txt) 的两个字母代码。

对于上面展示的 `Info.plist` 示例，`de.lproj > InfoPlist.strings` 文件可以写成这样：

```ini
NSCameraUsageDescription = "Kamera Zugriff wird benötigt für WebRTC Funktionalität";
NSMicrophoneUsageDescription = "Mikrofon Zugriff wird benötigt für WebRTC Funktionalität";
```

最后，通过上面提到的 resources 特性让 Tauri 拾取这些文件：

```json
{
  "bundle": {
    "resources": {
      "infoplist/**": "./"
    }
  }
}
```

## 授权（Entitlements）

授权（entitlement）是一种特殊的 Apple 配置键值对，相当于授予应用特定能力的权利或特权，
例如作为用户默认邮件客户端，以及使用 App Sandbox 特性。

授权会在应用签名时应用。更多信息请参阅[代码签名文档](../sign/1-macos/)。

要定义应用所需的授权，你必须创建授权文件并配置 Tauri 使用它。

1. 在 `src-tauri` 文件夹中创建 `Entitlements.plist` 文件，并配置应用所需的键值对：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>com.apple.security.app-sandbox</key>
    <true/>
</dict>
</plist>
```

2. 配置 Tauri 使用该 Entitlements.plist 文件：

```json
{
  "bundle": {
    "macOS": {
      "entitlements": "./Entitlements.plist"
    }
  }
}
```

更多信息请参阅[官方文档](https://developer.apple.com/documentation/bundleresources/entitlements)。

## 最低系统版本

默认情况下你的 Tauri 应用支持 macOS 10.13 及以上。如果你使用的 API 需要更新的 macOS 系统，并希望在应用程序包中强制该要求，
你可以配置 [`tauri.conf.json > bundle > macOS > minimumSystemVersion`](https://tauri.app/reference/config/#minimumsystemversion)：

```json
{
  "bundle": {
    "macOS": {
      "minimumSystemVersion": "12.0"
    }
  }
}
```

## 包含 macOS framework

如果你的应用运行需要额外的 macOS framework，可以在 [`tauri.conf.json > bundle > macOS > frameworks`](https://tauri.app/reference/config/#frameworks-1) 配置中列出它们。
framework 列表可以包含系统 framework，也可以包含自定义 framework 和 dylib 文件。

```json
{
  "bundle": {
    "macOS": {
      "frameworks": [
        "CoreAudio",
        "./libs/libmsodbcsql.18.dylib",
        "./frameworks/MyApp.framework"
      ]
    }
  }
}
```

{{% alert title="注意" %}}

- 引用系统 framework 时，可以直接使用它的名称（不带 .framework 扩展名），而不必用绝对路径
- 系统 framework 必须存在于 `$HOME/Library/Frameworks`、`/Library/Frameworks/` 或 `/Network/Library/Frameworks/` 之一
- 引用本地 framework 和 dylib 文件时，必须使用相对于 `src-tauri` 目录的完整路径

{{% /alert %}}

## 添加自定义文件

你可以使用 [`tauri.conf.json > bundle > macOS > files`](https://tauri.app/reference/config/#files-2) 配置向应用程序包添加自定义文件，
它把目标路径映射到相对于 `tauri.conf.json` 文件的源路径。
这些文件会被加入 `<product-name>.app/Contents` 文件夹。

```json
{
  "bundle": {
    "macOS": {
      "files": {
        "embedded.provisionprofile": "./profile-name.provisionprofile",
        "SharedSupport/docs.md": "./docs/index.md"
      }
    }
  }
}
```

在上面的示例中，`profile-name.provisionprofile` 文件会被复制到 `<product-name>.app/Contents/embedded.provisionprofile`，
`docs/index.md` 文件会被复制到 `<product-name>.app/Contents/SharedSupport/docs.md`。
