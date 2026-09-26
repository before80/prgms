+++
title = "7 Deep Linking"
date = 2026-09-25T21:31:08+08:00
weight = 7
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/plugin/deep-linking/](https://tauri.app/plugin/deep-linking/)

把你的 Tauri 应用设为某个 URL 的默认处理程序。

## 支持的平台

| 平台 | 支持程度 | 说明 |
| --- | --- | --- |
| Windows | 完整支持 |  |
| Linux | 完整支持 |  |
| macOS | 完整支持 |  |
| Android | 部分支持 |  |
| iOS | 部分支持 |  |

## 设置

### 自动

使用你的项目包管理器添加依赖：

{{< tabpane text=true persist=disabled >}}

{{% tab header="npm" %}}

```sh
npm run tauri add deep-link
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn run tauri add deep-link
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm tauri add deep-link
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno task tauri add deep-link
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun tauri add deep-link
```

{{% /tab %}}

{{% tab header="cargo" %}}

```sh
cargo tauri add deep-link
```

{{% /tab %}}

{{< /tabpane >}}

### 手动

1. 在 `src-tauri` 文件夹中运行以下命令，把插件加入 `Cargo.toml` 里的项目依赖：

   ```sh
   cargo add tauri-plugin-deep-link@2.0.0
   ```

2. 修改 `lib.rs` 初始化插件：

   ```rust
   #[cfg_attr(mobile, tauri::mobile_entry_point)]
   pub fn run() {
       tauri::Builder::default()
           .plugin(tauri_plugin_deep_link::init())
           .run(tauri::generate_context!())
           .expect("error while running tauri application");
   }
   ```

3. 用你偏好的 JavaScript 包管理器安装 JavaScript 端绑定：

{{< tabpane text=true persist=disabled >}}

{{% tab header="npm" %}}

```sh
npm install @tauri-apps/plugin-deep-link
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn add @tauri-apps/plugin-deep-link
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm add @tauri-apps/plugin-deep-link
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno add npm:@tauri-apps/plugin-deep-link
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun add @tauri-apps/plugin-deep-link
```

{{% /tab %}}

{{< /tabpane >}}


## 配置准备

### Android

在 Android 上有两种方式可以从链接打开你的应用：

1. **App Links（http/https + host，需验证）**
   对于 [app links](https://developer.android.com/training/app-links#android-app-links)，你需要一个带
   `.well-known/assetlinks.json` 端点的服务器，它必须返回给定格式的文本响应：

```json
[
  {
    "relation": ["delegate_permission/common.handle_all_urls"],
    "target": {
      "namespace": "android_app",
      "package_name": "$APP_BUNDLE_ID",
      "sha256_cert_fingerprints": [
        $CERT_FINGERPRINT
      ]
    }
  }
]
```

其中 `$APP_BUNDLE_ID` 是 [`tauri.conf.json > identifier`](https://tauri.app/reference/config/#identifier) 中定义的值，并把 `-` 替换为 `_`；
`$CERT_FINGERPRINT` 是你应用签名证书的 SHA256 指纹列表，
更多信息见[验证 Android applinks](https://developer.android.com/training/app-links/verify-android-applinks#web-assoc)。

2. **自定义 URI scheme（无需 host，无需验证）**
   对于 `myapp://...` 这样的 URI，你可以在不托管任何文件的情况下声明自定义 scheme。在移动端配置中使用 `scheme` 字段并省略 `host`。

### iOS

在 iOS 上有两种方式可以从链接打开你的应用：

1. **Universal Links（https + host，需验证）**
   对于 [universal links](https://developer.apple.com/documentation/xcode/allowing-apps-and-websites-to-link-to-your-content?language=objc)，你需要一个带 `.well-known/apple-app-site-association` 端点的服务器，它必须返回给定格式的 JSON 响应：

```json
{
  "applinks": {
    "details": [
      {
        "appIDs": ["$DEVELOPMENT_TEAM_ID.$APP_BUNDLE_ID"],
        "components": [
          {
            "/": "/open/*",
            "comment": "Matches any URL whose path starts with /open/"
          }
        ]
      }
    ]
  }
}
```

{{% alert title="注意" %}}
响应的 `Content-Type` 头必须是 `application/json`。

`.well-known/apple-app-site-association` 端点必须通过 HTTPS 提供。
要在 localhost 上测试，你可以使用自签名 TLS 证书并把它安装到 iOS 模拟器上，或者使用 [ngrok](https://ngrok.com/) 之类的服务。
{{% /alert %}}

其中 `$DEVELOPMENT_TEAM_ID` 是 `tauri.conf.json > bundle > iOS > developmentTeam` 或
`TAURI_APPLE_DEVELOPMENT_TEAM` 环境变量中定义的值，`$APP_BUNDLE_ID` 是 [`tauri.conf.json > identifier`](https://tauri.app/reference/config/#identifier) 中定义的值。

要验证你的域名是否已正确配置以暴露应用关联，你可以运行以下命令，把 `<host>` 替换为你实际的 host：

```sh
curl -v https://app-site-association.cdn-apple.com/a/v1/<host>
```

更多信息见 [applinks.details](https://developer.apple.com/documentation/bundleresources/applinks/details-swift.dictionary)。

2. **自定义 URI scheme（无 host，无验证）**
   对于 `myapp://...` 这样的 URI，你可以在移动端配置中声明自定义 scheme，并把 `"appLink": false`（或省略它）。插件会在应用的 Info.plist 中生成相应的 `CFBundleURLTypes` 条目。无需 `.well-known` 文件或 HTTPS host。

### 桌面端

在 Linux 和 Windows 上，深链接会作为命令行参数传给新的应用进程。
如果你希望由唯一的应用实例接收这些事件，deep link 插件与 [single instance](../24-singleinstance/) 插件有集成。

- 首先你必须为 single instance 插件添加 `deep-link` 特性：

```toml
[target."cfg(any(target_os = \"macos\", windows, target_os = \"linux\"))".dependencies]
tauri-plugin-single-instance = { version = "2.0.0", features = ["deep-link"] }
```

- 然后配置 single instance 插件，它应当始终是你注册的第一个插件：

```rust
#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    let mut builder = tauri::Builder::default();

    #[cfg(desktop)]
    {
        builder = builder.plugin(tauri_plugin_single_instance::init(|_app, argv, _cwd| {
          println!("a new app instance was opened with {argv:?} and the deep link event was already triggered");
          // 在运行时定义深链接 scheme 时，你也必须在这里检查 `argv`
        }));
    }

    builder = builder.plugin(tauri_plugin_deep_link::init());
}
```

{{% alert title="警告" color="warning" %}}
用户可以通过把 URL 作为参数手动触发一个假的深链接。
Tauri 会把命令行参数与所配置的 scheme 做匹配以缓解这一问题，
但你仍应检查该 URL 是否匹配你期望的格式。

这意味着 Tauri 只处理静态配置的 scheme 的深链接，
运行时注册的 scheme 必须用 [`Env::args_os`](https://docs.rs/tauri/2.0.0/tauri/struct.Env.html#structfield.args_os) 手动检查。
{{% /alert %}}

## 配置

在 `tauri.conf.json > plugins > deep-link` 下，配置你想要与你的应用关联的移动端域名／scheme 以及桌面端 scheme。

### 示例

**移动端自定义 scheme（无需服务器）：**

```json
{
  "plugins": {
    "deep-link": {
      "mobile": [
        {
          "scheme": ["ovi"],
          "appLink": false
        }
      ]
    }
  }
}
```

这会在 Android 和 iOS 上注册 `ovi://*` scheme。

**App Link / Universal Link（已验证的 https + host）：**

```json
{
  "plugins": {
    "deep-link": {
      "mobile": [
        {
          "scheme": ["https"],
          "host": "your.website.com",
          "pathPrefix": ["/open"],
          "appLink": true
        }
      ]
    }
  }
}
```

这会把 `https://your.website.com/open/*` 注册为 app/universal link。

**桌面端自定义 scheme：**

```json
{
  "plugins": {
    "deep-link": {
      "desktop": {
        "schemes": ["something", "my-tauri-app"]
      }
    }
  }
}
```

## 用法

deep-link 插件在 JavaScript 和 Rust 中都可以使用。

### 监听深链接

**语言**

{{< tabpane text=true persist=disabled >}}

{{% tab header="JavaScript" %}}

当应用正在运行时被深链接触发，`onOpenUrl` 回调会被调用。要检测你的应用是否是通过深链接打开的，请在应用启动时使用 `getCurrent`。

```javascript
import { getCurrent, onOpenUrl } from '@tauri-apps/plugin-deep-link';
// 使用 `"withGlobalTauri": true` 时，你可以这样写
// const { getCurrent, onOpenUrl } = window.__TAURI__.deepLink;

const startUrls = await getCurrent();
if (startUrls) {
  // 应用很可能是通过深链接启动的
  // 注意 getCurrent 的返回值也会在每次 onOpenUrl 触发时更新。
}

await onOpenUrl((urls) => {
  console.log('deep link:', urls);
});
```

{{% /tab %}}

{{% tab header="Rust" %}}

当应用正在运行时被深链接触发，插件的 `on_open_url` 闭包会被调用。要检测你的应用是否是通过深链接打开的，请在应用启动时使用 `get_current`。

```rust
use tauri_plugin_deep_link::DeepLinkExt;

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_deep_link::init())
        .setup(|app| {
            // 注意 get_current 的返回值也会在每次 on_open_url 触发时更新。
            let start_urls = app.deep_link().get_current()?;
            if let Some(urls) = start_urls {
                // 应用很可能是通过深链接启动的
                println!("deep link URLs: {:?}", urls);
            }

            app.deep_link().on_open_url(|event| {
                println!("deep link URLs: {:?}", event.urls());
            });
            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

{{% /tab %}}

{{< /tabpane >}}

{{% alert title="注意" %}}
打开 URL 事件会带一个 URL 列表触发，这是为了与 macOS 的深链接 API 保持兼容，
但大多数情况下你的应用只会收到单个 URL。
{{% /alert %}}

### 在运行时注册桌面端深链接

[配置](#配置)一节介绍了如何为你的应用定义静态深链接 scheme。

在 Linux 和 Windows 上，还可以通过 `register` Rust 函数在运行时把 scheme 与你的应用关联。

在下面的片段中，我们将在运行时注册 `my-app` scheme。第一次执行应用之后，
操作系统就会用我们的应用打开 `my-app://*` URL：

```rust
use tauri_plugin_deep_link::DeepLinkExt;

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_deep_link::init())
        .setup(|app| {
            #[cfg(desktop)]
            app.deep_link().register("my-app")?;
            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

{{% alert title="注意" %}}
在运行时注册深链接对在 Linux 和 Windows 上开发很有用，
因为默认情况下只有你的应用被安装时才会注册深链接。

安装 AppImage 可能比较复杂，因为它需要 AppImage 启动器。

运行时注册深链接可能更可取，因此 Tauri 也提供了一个辅助函数，用于在运行时强制注册所有静态配置的深链接。
调用该函数也能确保深链接在开发模式下被注册：

```rust
#[cfg(any(target_os = "linux", all(debug_assertions, windows)))]
{
  use tauri_plugin_deep_link::DeepLinkExt;
  app.deep_link().register_all()?;
}
```

{{% /alert %}}

## 测试

为你的应用测试深链接有一些注意事项。

### 桌面端

在桌面端，深链接只会为已安装的应用触发。
在 Linux 和 Windows 上，你可以用 [`register_all`](https://docs.rs/tauri-plugin-deep-link/2.0.0/tauri_plugin_deep_link/struct.DeepLink.html#method.register_all) Rust 函数绕过这一点，
它把所有配置的 scheme 注册为触发当前可执行文件：

```rust
use tauri_plugin_deep_link::DeepLinkExt;

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_deep_link::init())
        .setup(|app| {
            #[cfg(any(windows, target_os = "linux"))]
            {
                use tauri_plugin_deep_link::DeepLinkExt;
                app.deep_link().register_all()?;
            }
            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

{{% alert title="注意" %}}
在 Linux 上安装支持深链接的 AppImage 需要一个 AppImage 启动器，以便把 AppImage 与操作系统集成。
使用 `register_all` 函数，你就可以开箱即用地支持深链接，而无需用户使用外部工具。

当 AppImage 被移动到文件系统中的其它位置时，深链接会失效，因为它利用了可执行文件的绝对路径，
这使得在运行时注册 scheme 更加重要。

更多信息见[在运行时注册桌面端深链接](#在运行时注册桌面端深链接)一节。
{{% /alert %}}

{{% alert title="警告" color="warning" %}}
在 macOS 上无法在运行时注册深链接，因此深链接只能在打包后的应用上测试，
而该应用必须安装在 `/Applications` 目录中。
{{% /alert %}}

#### Windows

要在 Windows 上触发深链接，你既可以在浏览器中打开 `<scheme>://url`，也可以在终端中运行以下命令：

```sh
start <scheme>://url
```

#### Linux

要在 Linux 上触发深链接，你既可以在浏览器中打开 `<scheme>://url`，也可以在终端中运行 `xdg-open`：

```sh
xdg-open <scheme>://url
```

### iOS

要在 iOS 上触发 app link，你可以在浏览器中打开 `https://<host>/path` URL。对于模拟器，你可以利用 `simctl` CLI 直接从终端打开链接：

```sh
xcrun simctl openurl booted https://<host>/path
```

### Android

要在 Android 上触发 app link，你可以在浏览器中打开 `https://<host>/path` URL。对于模拟器，你可以利用 `adb` CLI 直接从终端打开链接：

```sh
adb shell am start -a android.intent.action.VIEW -d https://<host>/path <bundle-identifier>
```

## 权限

默认情况下，所有有潜在危险的插件命令和作用域都被阻止，无法访问。你必须在 `capabilities` 配置中修改权限才能启用它们。

更多信息请参阅[能力概述](../../security/4-capabilities/)，以及[使用插件权限的分步指南](../../learn/security/1-usingpluginpermissions/)。

```json
{
  "$schema": "../gen/schemas/mobile-schema.json",
  "identifier": "mobile-capability",
  "windows": ["main"],
  "platforms": ["iOS", "android"],
  "permissions": [
    // 通常你需要 core:event:default 来监听 deep-link 事件
    "core:event:default",
    "deep-link:default"
  ]
}
```
