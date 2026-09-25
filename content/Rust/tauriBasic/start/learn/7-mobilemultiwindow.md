+++
title = "7 移动端多窗口"
date = 2026-09-25T21:31:08+08:00
weight = 7
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/learn/mobile-multiwindow/](https://tauri.app/learn/mobile-multiwindow/)

Tauri 在 Android 和 iOS 上支持多窗口，让你的应用可以在平板上并排显示内容，或在 iPad 上以独立场景（scene）显示。

在 **Android** 上，多窗口是通过 [Activity Embedding](https://developer.android.com/guide/topics/large-screens/activity-embedding) 实现的，它让系统可以在大屏上并排显示两个 activity。

在 **iOS** 上，多窗口使用 [UIScene](https://developer.apple.com/documentation/uikit/uiscene) API，它允许 iPad 用户在独立窗口中打开应用的多个实例。

在**手机**上，系统通常不会把两个窗口并排布局。在 **Android** 上，创建另一个窗口仍会启动一个独立的 activity，但在手机尺寸的屏幕上它通常会被**压入 activity 返回栈**——因此按 **Back** 会返回上一个 activity，而不是关闭分屏。在 **iOS** 上（尤其是 iPhone），打开或创建另一个窗口往往会用新场景的内容**替换当前 UI**，而不是让两者同时可见；真正并发的窗口仍然是 **iPad**（以及 Stage Manager）的体验。

{{% alert title="注意" %}}
多窗口需要 Android 12L (API 32)+ 和 iOS 13+。你可以在运行时用 [`app.supportsMultipleWindows`](https://tauri.app/reference/javascript/api/namespaceapp/#supportsmultiplewindows) API 检查可用性。
{{% /alert %}}

## 共同的前置设置

两个平台都需要一项能力（capability）权限才能从前端创建新窗口。

### 能力

把 `core:webview:allow-create-webview-window` 权限加入你的能力文件，这样前端才能创建新窗口。

如果你要创建多个窗口，请使用通配符，或在 `windows` 数组中列出每个窗口标签：

```json
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "default",
  "description": "Capability for the main window",
  "windows": ["main"],
  "permissions": ["core:default", "core:webview:allow-create-webview-window"]
}
```

## Android

Android 多窗口使用 [Activity Embedding](https://developer.android.com/guide/topics/large-screens/activity-embedding)，在大屏（平板、折叠屏）上把 activity 分屏并排显示。你需要为每种窗口类型创建一个 Android `Activity`、配置分屏规则，并注册一个 initializer。

### 1. 添加依赖

把所需的 AndroidX 库加入你的 `build.gradle.kts`：

```kotlin
dependencies {
    // ... 已有依赖
    implementation("androidx.window:window:1.5.0")
    implementation("androidx.startup:startup-runtime:1.2.0")
}
```

### 2. 创建新的 Activity

为每个额外的窗口类型创建一个 Kotlin 类。每个 activity 都必须继承 `TauriActivity`：

```kotlin

import android.os.Bundle
import android.os.PersistableBundle

class DetailActivity: TauriActivity() {
  override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)
  }
}
```

### 3. 更新 AndroidManifest.xml

注册新的 activity，并通过添加 `tools` 命名空间和 embedding 属性来启用 activity embedding：

```xml
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
  xmlns:tools="http://schemas.android.com/tools">

  <application ...>

    <property
      android:name="android.window.PROPERTY_ACTIVITY_EMBEDDING_SPLITS_ENABLED"
      android:value="true" />

    <!-- 已有的 MainActivity -->
    <activity
      android:name=".MainActivity"
      android:exported="true"
      ...>
      ...
    </activity>

    <!-- 用于详情窗口的新 activity -->
    <activity android:name=".DetailActivity" android:exported="true" />

    <!-- 注册分屏 initializer -->
    <provider android:name="androidx.startup.InitializationProvider"
      android:authorities="${applicationId}.androidx-startup"
      android:exported="false"
      tools:node="merge">
      <meta-data android:name="${applicationId}.SplitInitializer"
        android:value="androidx.startup" />
    </provider>

  </application>
</manifest>
```

### 4. 创建分屏 Initializer

该 initializer 在应用启动时加载分屏配对规则：

```kotlin

import android.content.Context
import androidx.startup.Initializer
import androidx.window.core.ExperimentalWindowApi
import androidx.window.embedding.RuleController

@OptIn(ExperimentalWindowApi::class)
class SplitInitializer : Initializer<RuleController> {
  override fun create(context: Context): RuleController {
    return RuleController.getInstance(context).apply {
      setRules(RuleController.parseRules(context, R.xml.main_split_config))
    }
  }

  override fun dependencies(): List<Class<out Initializer<*>>> {
    return emptyList()
  }
}
```

### 5. 定义分屏规则

创建一个 XML 资源，告诉系统如何配对 activity 并分屏：

```xml
  xmlns:window="http://schemas.android.com/apk/res-auto">

  <SplitPairRule
    window:splitRatio="0.33"
    window:splitLayoutDirection="locale"
    window:splitMinWidthDp="840"
    window:splitMaxAspectRatioInPortrait="alwaysAllow"
    window:finishPrimaryWithSecondary="never"
    window:finishSecondaryWithPrimary="never"
    window:clearTop="false">
    <SplitPairFilter
      window:primaryActivityName=".MainActivity"
      window:secondaryActivityName=".DetailActivity"/>
  </SplitPairRule>

</resources>
```

关键属性：
- `splitRatio` —— 屏幕如何分割（0.33 表示主 activity 占三分之一）
- `splitMinWidthDp` —— 激活分屏的最小屏幕宽度（840dp 面向平板）
- `splitMaxAspectRatioInPortrait` —— 设为 `alwaysAllow` 可在竖屏模式下启用分屏
- `primaryActivityName` / `secondaryActivityName` —— 哪一对 activity 触发分屏

## iOS

在 iOS 上，多窗口使用 UIScene API。iPad 用户可以通过长按应用图标并选择 “New window” 来打开新窗口，你的应用也可以以编程方式创建它们。

### 1. 启用 Scene 支持

在你的 `src-tauri` 目录中创建 `Info.ios.plist` 文件来声明 scene 支持：

```xml
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>UIApplicationSceneManifest</key>
  <dict>
    <key>UIApplicationSupportsMultipleScenes</key>
    <true/>
    <key>UISceneConfigurations</key>
    <dict/>
  </dict>
</dict>
</plist>
```

### 2. 处理 Scene 请求

当用户在 iPad 上请求新窗口时（例如长按应用图标），Tauri 会发出 `RunEvent::SceneRequested` 事件。处理它以创建新窗口：

```rust
pub fn run() {
    #[cfg(target_os = "ios")]
    let mut counter = 0;

    tauri::Builder::default()
        .setup(|app| {
            tauri::WebviewWindowBuilder::new(
                app, "main", tauri::WebviewUrl::default()
            ).build()?;
            Ok(())
        })
        .build(tauri::generate_context!())
        .expect("error while running tauri application")
        .run(move |app, event| {
            #[cfg(target_os = "ios")]
            if let tauri::RunEvent::SceneRequested { .. } = event {
                counter += 1;
                tauri::WebviewWindowBuilder::new(
                    app,
                    format!("main-{counter}"),
                    tauri::WebviewUrl::default(),
                )
                .build()
                .unwrap();
            }
            #[cfg(not(target_os = "ios"))]
            let _ = (app, event);
        });
}
```

{{% alert title="注意" %}}
由于 scene 请求创建的窗口使用 `main-1`、`main-2` 这样的动态标签，请确保你的能力文件包含覆盖它们的通配模式——例如 `"windows": ["main", "main-*"]`。
{{% /alert %}}

## 创建窗口

你既可以从 Rust 创建额外窗口，也可以从前端 JavaScript API 创建。`WebviewWindowBuilder`（Rust）和 `WebviewWindow`（JavaScript）都接受平台特定的选项：

Android 选项：

- `activityName` —— 为该窗口创建的 Android Activity 类名。
- `createdByActivityName` —— 正在创建该窗口的 Activity 名称。它决定新 activity 属于哪个 activity 栈，这对分屏规则正确工作很重要。未设置时，它会自动从 manager 继承（例如从 `Window` 或 `Webview` 句柄构建时）。

iOS 选项：

- `requestedBySceneIdentifier` —— 设置正在请求创建这个新 scene 的 UIScene 标识符，从而在两个 scene 之间建立关系。默认情况下系统使用前台 scene。未设置时，它会自动从 manager 继承。

**语言**

{{< tabpane text=true persist=disabled >}}
{{% tab header="JavaScript" %}}

```javascript
import { WebviewWindow } from '@tauri-apps/api/webviewWindow';

function openDetail(id) {
  const webview = new WebviewWindow(`detail-${id}`, {
    url: `detail/${id}`,
    activityName: 'DetailActivity',
  });
  webview.once('tauri://created', () => {
    console.log('window created');
  });
  webview.once('tauri://error', (e) => {
    console.error(e);
  });
}
```

{{% /tab %}}

{{% tab header="Rust" %}}

```rust

let main_window = app.get_webview_window("main").unwrap();
// 使用 main_window 实例，这样关系会被自动确定
let builder = tauri::WebviewWindowBuilder::new(main_window, "detail", tauri::WebviewUrl::App("detail/1".into()));

#[cfg(target_os = "android")]
let builder = builder.activity_name("DetailActivity");

let window = builder.build()?;
```

{{% /tab %}}

{{< /tabpane >}}
{{% alert title="提示" %}}
如果你使用前端路由，请使用基于浏览器历史的路由（例如 React Router 中的 `createBrowserRouter`）而不是 hash 路由，这样每个窗口才能导航到不同的 URL 路径。
{{% /alert %}}

## 窗口实例 API

窗口创建之后，你可以获取它平台特定的标识符：

**语言**

{{< tabpane text=true persist=disabled >}}
{{% tab header="JavaScript" %}}

```javascript
const sceneId = await window.sceneIdentifier();
```

{{% /tab %}}

{{% tab header="Rust" %}}

```rust
let activity = window.activity_name()?;

#[cfg(target_os = "ios")]
let scene_id = window.scene_identifier()?;
```

{{% /tab %}}

{{< /tabpane >}}
这些 getter 在创建相关窗口时用于引用某个窗口的身份很有用。例如，你可以读取某个窗口的 `activityName` 并把它作为新窗口的 `createdByActivityName` 传入，或者读取 `sceneIdentifier` 并作为 `requestedBySceneIdentifier` 传入。
