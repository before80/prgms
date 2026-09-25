+++
title = "8 移动端文件关联"
date = 2026-09-25T21:31:08+08:00
weight = 8
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/learn/mobile-file-associations/](https://tauri.app/learn/mobile-file-associations/)

Tauri 在 Android 和 iOS 上支持文件关联，让你的应用可以注册为特定文件类型的处理程序。当用户打开与你声明的关联匹配的文件时，操作系统会启动你的应用并传入该文件 URL。

在 **Android** 上，文件关联通过 Tauri 构建系统根据你的配置自动生成的 [intent filter](https://developer.android.com/training/app-links/deep-linking) 实现。

在 **iOS** 上，文件关联使用 [CFBundleDocumentTypes](https://developer.apple.com/documentation/bundleresources/information-property-list/cfbundledocumenttypes)，对自定义文件类型还可选使用 [UTExportedTypeDeclarations](https://developer.apple.com/documentation/bundleresources/information-property-list/utexportedtypedeclarations)。

## 配置

文件关联在 `tauri.conf.json` 的 `bundle.fileAssociations` 下声明。Tauri CLI 使用该配置生成相应的平台特定元数据（`AndroidManifest.xml` 中的 Android intent filter、`Info.plist` 中的 iOS document type）。

数组中的每一项代表你的应用可以处理的一种文件类型：

```json
{
  "bundle": {
    "fileAssociations": [
      {
        "ext": ["png"],
        "mimeType": "image/png"
      },
      {
        "ext": ["jpg", "jpeg"],
        "mimeType": "image/jpeg"
      }
    ]
  }
}
```

### 配置选项

- `ext` —— 要关联的文件扩展名列表（不带前导点）。
- `mimeType` —— 该文件的 MIME 类型（例如 `image/png`）。在 Android 上进行 intent filter 匹配时是必需的。未指定时，Tauri 会根据扩展名推断常见的 MIME 类型。
- `role` —— 应用相对于该文件类型的角色。在 Apple 平台上映射为 `CFBundleTypeRole`。取值：`Editor`（默认）、`Viewer`、`Shell`、`QLGenerator`、`None`。
- `rank` —— 在处理该文件类型的应用中的排名。在 Apple 平台上映射为 `LSHandlerRank`。取值：`Default`（默认）、`Owner`、`Alternate`、`None`。
- `name` —— 该文件类型的显示名称。默认使用第一个扩展名。
- `exportedType` —— 定义由你的应用拥有的自定义文件类型。在 Apple 平台上关联非标准文件扩展名时必需。
- `androidIntentActionFilters` —— 要注册哪些 Android intent action。取值：`Send`、`SendMultiple`、`View`。默认三者全部使用。

### 自定义文件类型

对于非标准文件扩展名，你应当定义 `exportedType`，以便 Apple 平台能识别该文件类型。`identifier` 应当是一个对你的应用唯一的反向 DNS 字符串，`conformsTo` 列出父类型：

```json
{
  "bundle": {
    "fileAssociations": [
      {
        "ext": ["mydata"],
        "mimeType": "application/octet-stream",
        "exportedType": {
          "identifier": "com.example.myapp.mydata",
          "conformsTo": ["public.data"]
        }
      }
    ]
  }
}
```

常见的 `conformsTo` 取值包括 `public.data`、`public.image`、`public.json` 和 `public.plain-text`。

## 处理被打开的文件

当用你的应用打开一个文件时，Tauri 会发出包含文件 URL 的 `RunEvent::Opened` 事件。该事件在 macOS、iOS 和 Android 上都可用。

你需要处理两种情况：

1. **应用已在运行** —— 事件在运行时投递。
2. **应用由打开文件而启动** —— 事件在启动期间触发，因此你应当保存这些 URL，并让前端可以获取它们。

### Rust

把传入的 URL 存进托管的 state，通过一个命令暴露给前端在启动时调用，并在每次 `RunEvent::Opened` 触发时发出一个 Tauri 事件，这样应用已经在运行时前端也能立即响应：

```rust
use tauri::Manager;

struct OpenedUrls(Mutex<Vec<tauri::Url>>);

#[tauri::command]
fn opened_urls(app: tauri::AppHandle) -> Vec<tauri::Url> {
    app.state::<OpenedUrls>().0.lock().unwrap().clone()
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .manage(OpenedUrls(Mutex::new(vec![])))
        .invoke_handler(tauri::generate_handler![opened_urls])
        .build(tauri::generate_context!())
        .expect("error while running tauri application")
        .run(|app, event| {
            #[cfg(any(target_os = "macos", target_os = "ios", target_os = "android"))]
            if let tauri::RunEvent::Opened { urls } = event {
                use tauri::Emitter;
                app.state::<OpenedUrls>()
                    .0
                    .lock()
                    .unwrap()
                    .extend(urls.clone());
                app.emit("opened", urls).unwrap();
            }
        });
}
```

### JavaScript

下面的前端在两方面与那段 Rust 代码配合：

- **`invoke('opened_urls')`** 调用 `opened_urls` 命令，因此 webview 可以读取在 UI 加载完成之前（由打开文件触发的冷启动）就已存入的 URL。
- **`listen('opened', …)`** 订阅的事件名与 Rust 中传给 **`app.emit("opened", urls)`** 的一致，因此应用已在运行时触发的文件打开事件会被立即投递。

```javascript
import { listen } from '@tauri-apps/api/event';
import { invoke } from '@tauri-apps/api/core';

// 冷启动：URL 可能在前端加载之前就已经存在于 Rust state 中
const initialUrls = await invoke('opened_urls');
if (initialUrls.length > 0) {
  handleFiles(initialUrls);
}

// 热启动：RunEvent::Opened 触发时 Rust 会发出 "opened" 事件
await listen('opened', (event) => {
  handleFiles(event.payload);
});
```
