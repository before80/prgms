+++
title = "4 Biometric"
date = 2026-09-25T21:31:08+08:00
weight = 4
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/plugin/biometric/](https://tauri.app/plugin/biometric/)

在 Android 和 iOS 上向用户发起生物识别认证。

## 支持的平台

| 平台 | 支持程度 | 说明 |
| --- | --- | --- |
| Windows | 不支持 |  |
| Linux | 不支持 |  |
| macOS | 不支持 |  |
| Android | 完整支持 |  |
| iOS | 完整支持 |  |

## 设置

### 自动

使用你的项目包管理器添加依赖：

{{< tabpane text=true persist=disabled >}}

{{% tab header="npm" %}}

```sh
npm run tauri add biometric
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn run tauri add biometric
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm tauri add biometric
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno task tauri add biometric
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun tauri add biometric
```

{{% /tab %}}

{{% tab header="cargo" %}}

```sh
cargo tauri add biometric
```

{{% /tab %}}

{{< /tabpane >}}

### 手动

1. 在 `src-tauri` 文件夹中运行以下命令，把插件加入 `Cargo.toml` 里的项目依赖：

   ```sh
   cargo add tauri-plugin-biometric --target 'cfg(any(target_os = "android", target_os = "ios"))'
   ```

2. 修改 `lib.rs` 初始化插件：

   ```rust
   #[cfg_attr(mobile, tauri::mobile_entry_point)]
   pub fn run() {
       tauri::Builder::default()
           .setup(|app| {
               #[cfg(mobile)]
               app.handle().plugin(tauri_plugin_biometric::Builder::new().build());
               Ok(())
           })
           .run(tauri::generate_context!())
           .expect("error while running tauri application");
   }
   ```

3. 用你偏好的 JavaScript 包管理器安装 JavaScript 端绑定：

{{< tabpane text=true persist=disabled >}}

{{% tab header="npm" %}}

```sh
npm install @tauri-apps/plugin-biometric
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn add @tauri-apps/plugin-biometric
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm add @tauri-apps/plugin-biometric
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno add npm:@tauri-apps/plugin-biometric
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun add @tauri-apps/plugin-biometric
```

{{% /tab %}}

{{< /tabpane >}}


## 配置

在 iOS 上，biometric 插件需要 `NSFaceIDUsageDescription` 信息属性列表值，它应当说明你的应用为什么需要使用生物识别认证。

在 `src-tauri/Info.ios.plist` 文件中加入以下片段：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
	<dict>
		<key>NSFaceIDUsageDescription</key>
		<string>Authenticate with biometric</string>
	</dict>
</plist>
```

## 用法

该插件让你可以验证设备上生物识别认证是否可用、向用户发起生物识别认证，并检查结果以判断认证是否成功。

### 检查状态

你可以检查生物识别认证的状态，包括它是否可用以及支持哪些生物识别认证方式。

**语言**

{{< tabpane text=true persist=disabled >}}

{{% tab header="JavaScript" %}}

```javascript
import { checkStatus } from '@tauri-apps/plugin-biometric';

const status = await checkStatus();
if (status.isAvailable) {
  console.log('Yes! Biometric Authentication is available');
} else {
  console.log(
    'No! Biometric Authentication is not available due to ' + status.error
  );
}
```

{{% /tab %}}

{{% tab header="Rust" %}}

```rust
use tauri_plugin_biometric::BiometricExt;

fn check_biometric(app_handle: tauri::AppHandle) {
    let status = app_handle.biometric().status().unwrap();
    if status.is_available {
        println!("Yes! Biometric Authentication is available");
    } else {
        println!("No! Biometric Authentication is not available due to: {}", status.error.unwrap());
    }
}
```

{{% /tab %}}

{{< /tabpane >}}

### 认证

要向用户发起生物识别认证，请使用 `authenticate()` 方法。

**语言**

{{< tabpane text=true persist=disabled >}}

{{% tab header="JavaScript" %}}

```javascript
import { authenticate } from '@tauri-apps/plugin-biometric';

const options = {
  // 若希望用户可以使用手机密码认证，请设为 true
  allowDeviceCredential: false,
  cancelTitle: "Feature won't work if Canceled",

  // 仅 iOS 的特性
  fallbackTitle: 'Sorry, authentication failed',

  // 仅 Android 的特性
  title: 'Tauri feature',
  subtitle: 'Authenticate to access the locked Tauri function',
  confirmationRequired: true,
};

try {
  await authenticate('This feature is locked', options);
  console.log(
    'Hooray! Successfully Authenticated! We can now perform the locked Tauri function!'
  );
} catch (err) {
  console.log('Oh no! Authentication failed because ' + err.message);
}
```

{{% /tab %}}

{{% tab header="Rust" %}}

```rust
use tauri_plugin_biometric::{BiometricExt, AuthOptions};

fn bio_auth(app_handle: tauri::AppHandle) {

    let options = AuthOptions {
        // 若希望用户可以使用手机密码认证，请设为 true
        allow_device_credential:false,
        cancel_title: Some("Feature won't work if Canceled".to_string()),

        // 仅 iOS 的特性
        fallback_title: Some("Sorry, authentication failed".to_string()),

        // 仅 Android 的特性
        title: Some("Tauri feature".to_string()),
        subtitle: Some("Authenticate to access the locked Tauri function".to_string()),
        confirmation_required: Some(true),
    };

    // 如果认证成功，函数返回 Result::Ok()
    // 否则返回 Result::Error()
    match app_handle.biometric().authenticate("This feature is locked".to_string(), options) {
        Ok(_) => {
            println!("Hooray! Successfully Authenticated! We can now perform the locked Tauri function!");
        }
        Err(e) => {
            println!("Oh no! Authentication failed because : {e}");
        }
    }
}
```

{{% /tab %}}

{{< /tabpane >}}

## 权限

默认情况下，所有有潜在危险的插件命令和作用域都被阻止，无法访问。你必须在 `capabilities` 配置中修改权限才能启用它们。

更多信息请参阅[能力概述](../../security/4-capabilities/)，以及[使用插件权限的分步指南](../../learn/security/1-usingpluginpermissions/)。

```json
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "main-capability",
  "description": "Capability for the main window",
  "windows": ["main"],
  "permissions": ["biometric:default"]
}
```
