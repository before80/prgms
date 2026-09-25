+++
title = "2 移动端插件开发"
date = 2026-09-25T21:31:08+08:00
weight = 2
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/develop/plugins/develop-mobile/](https://tauri.app/develop/plugins/develop-mobile/)

{{% alert title="插件开发" %}}

请确保你熟悉[插件开发指南](../1-overview/)中涵盖的概念，因为本指南中的许多概念都建立在那里所讲的基础之上。

{{% /alert %}}

插件可以运行用 Kotlin（或 Java）和 Swift 编写的原生移动端代码。默认插件模板包含一个使用 Kotlin 的 Android 库项目和一个 Swift 包，其中还包含一个示例移动端命令，演示如何从 Rust 代码触发它的执行。

## 初始化插件项目

按照[插件开发指南](../1-overview/#初始化插件项目)中的步骤初始化一个新的插件项目。

如果你已有插件并想为它添加 Android 或 iOS 能力，可以使用 `plugin android init` 和 `plugin ios init` 来引导生成移动端库项目，并指导你完成所需的改动。

默认插件模板把插件实现拆分为两个独立模块：`desktop.rs` 和 `mobile.rs`。

桌面端实现用 Rust 代码实现功能，而移动端实现则向原生移动端代码发送消息，执行某个函数并取回结果。如果两个实现之间需要共享逻辑，可以定义在 `lib.rs` 中：

```rust

impl<R: Runtime> <plugin-name><R> {
  pub fn do_something(&self) {
    // 做一件在桌面端和移动端之间共享的事情
  }
}
```

这种实现方式简化了共享 API 的过程，使其既能被命令使用，也能被 Rust 代码使用。

### 开发 Android 插件

Android 的 Tauri 插件被定义为继承 `app.tauri.plugin.Plugin` 并用 `app.tauri.annotation.TauriPlugin` 注解的 Kotlin 类。每个用 `app.tauri.annotation.Command` 注解的方法都可以被 Rust 或 JavaScript 调用。

Tauri 默认使用 Kotlin 实现 Android 插件，但如果你偏好 Java 也可以切换。生成插件后，在 Android Studio 中右键该 Kotlin 插件类，从菜单中选择 “Convert Kotlin file to Java file” 选项。Android Studio 会引导你完成向 Java 的项目迁移。

### 开发 iOS 插件

iOS 的 Tauri 插件被定义为继承 `Tauri` 包中 `Plugin` 类的 Swift 类。每个带有 `@objc` 属性和 `(_ invoke: Invoke)` 参数的函数（例如 `@objc private func download(_ invoke: Invoke) { }`）都可以被 Rust 或 JavaScript 调用。

插件被定义为一个 [Swift 包](https://www.swift.org/package-manager/)，因此你可以用它的包管理器管理依赖。

## 插件配置

关于开发插件配置的更多细节，请参阅插件开发指南的[插件配置一节](../1-overview/#插件配置)。

移动端的插件实例提供了一个获取插件配置的 getter：

**移动端操作系统**

{{< tabpane text=true persist=disabled >}}
{{% tab header="Android" %}}

```kotlin
import android.webkit.WebView
import app.tauri.annotation.TauriPlugin
import app.tauri.annotation.InvokeArg

@InvokeArg
class Config {
    var timeout: Int? = 3000
}

@TauriPlugin
class ExamplePlugin(private val activity: Activity): Plugin(activity) {
  private var timeout: Int? = 3000

  override fun load(webView: WebView) {
    getConfig(Config::class.java).let {
       this.timeout = it.timeout
    }
  }
}
```

{{% /tab %}}

{{% tab header="iOS" %}}

```swift
struct Config: Decodable {
  let timeout: Int?
}

class ExamplePlugin: Plugin {
  var timeout: Int? = 3000

  @objc public override func load(webview: WKWebView) {
    do {
      let config = try parseConfig(Config.self)
      self.timeout = config.timeout
    } catch {}
  }
}
```

{{% /tab %}}

{{< /tabpane >}}
## 生命周期事件

插件可以挂接到若干生命周期事件：

- [load](#load)：插件被加载进 web view 时
- [onNewIntent](#onnewintent)：仅 Android，activity 被重新启动时

插件开发指南中还有额外的[插件生命周期事件](../1-overview/#生命周期事件)。

### load

- **时机**：插件被加载进 web view 时
- **用途**：执行插件初始化代码

**移动端操作系统**

{{< tabpane text=true persist=disabled >}}
{{% tab header="Android" %}}

```kotlin
import android.webkit.WebView
import app.tauri.annotation.TauriPlugin

@TauriPlugin
class ExamplePlugin(private val activity: Activity): Plugin(activity) {
  override fun load(webView: WebView) {
    // 在这里执行插件设置
  }
}
```

{{% /tab %}}

{{% tab header="iOS" %}}

```swift
class ExamplePlugin: Plugin {
  @objc public override func load(webview: WKWebView) {
    let timeout = self.config["timeout"] as? Int ?? 30
  }
}
```

{{% /tab %}}

{{< /tabpane >}}
### onNewIntent

**注意**：仅在 Android 上可用。

- **时机**：activity 被重新启动时。更多信息见 [Activity#onNewIntent](https://developer.android.com/reference/android/app/Activity#onNewIntent(android.content.Intent))。
- **用途**：处理应用被重新启动的情况，例如点击通知或访问深链接时。

```kotlin
import android.content.Intent
import app.tauri.annotation.TauriPlugin

@TauriPlugin
class ExamplePlugin(private val activity: Activity): Plugin(activity) {
  override fun onNewIntent(intent: Intent) {
    // 处理新的 intent 事件
  }
}
```

## 添加移动端命令

在各自的移动端项目中都有一个插件类，可以在其中定义可由 Rust 代码调用的命令：

**移动端操作系统**

{{< tabpane text=true persist=disabled >}}
{{% tab header="Android" %}}

```kotlin
import app.tauri.annotation.Command
import app.tauri.annotation.TauriPlugin

@TauriPlugin
class ExamplePlugin(private val activity: Activity): Plugin(activity) {
  @Command
  fun openCamera(invoke: Invoke) {
    val ret = JSObject()
    ret.put("path", "/path/to/photo.jpg")
    invoke.resolve(ret)
  }
}
```

如果你想使用 Kotlin 的 `suspend` 函数，需要使用自定义的 coroutine scope：

```kotlin
import app.tauri.annotation.Command
import app.tauri.annotation.TauriPlugin

// 如果目的是获取数据，请改为 Dispatchers.IO
val scope = CoroutineScope(Dispatchers.Default + SupervisorJob())

@TauriPlugin
class ExamplePlugin(private val activity: Activity): Plugin(activity) {
  @Command
  fun openCamera(invoke: Invoke) {
    scope.launch {
      openCameraInner(invoke)
    }
  }

  private suspend fun openCameraInner(invoke: Invoke) {
    val ret = JSObject()
    ret.put("path", "/path/to/photo.jpg")
    invoke.resolve(ret)
  }
}
```

{{% alert title="注意" %}}
在 Android 上，原生命令被调度到主线程执行。执行长时间运行的操作会导致 UI 冻结，并可能触发 “Application Not Responding”（ANR）错误。

如果你需要等待某些阻塞式 IO，可以这样启动一个 coroutine：

```kotlin
CoroutineScope(Dispatchers.IO).launch {
  val result = myLongRunningOperation()
  invoke.resolve(result)
}
```

{{% /alert %}}

{{% /tab %}}

{{% tab header="iOS" %}}

```swift
class ExamplePlugin: Plugin {
	@objc public func openCamera(_ invoke: Invoke) throws {
    invoke.resolve(["path": "/path/to/photo.jpg"])
	}
}
```

{{% /tab %}}

{{< /tabpane >}}
使用 [`tauri::plugin::PluginHandle`](https://docs.rs/tauri/2.0.0/tauri/plugin/struct.PluginHandle.html) 从 Rust 调用移动端命令：

```rust
use serde::{Deserialize, Serialize};
use tauri::Runtime;

#[derive(Serialize)]
#[serde(rename_all = "camelCase")]
pub struct CameraRequest {
  quality: usize,
  allow_edit: bool,
}

#[derive(Deserialize)]
pub struct Photo {
  path: PathBuf,
}


impl<R: Runtime> <plugin-name;pascal-case><R> {
  pub fn open_camera(&self, payload: CameraRequest) -> crate::Result<Photo> {
    self
      .0
      .run_mobile_plugin("openCamera", payload)
      .map_err(Into::into)
  }
}
```

## 命令参数

参数会被序列化传给命令，可以在移动端插件中用 `Invoke::parseArgs` 函数解析，它接收一个描述参数对象的类。

### Android

在 Android 上，参数被定义为用 `@app.tauri.annotation.InvokeArg` 注解的类。内部对象也必须加注解：

```kotlin
import android.webkit.WebView
import app.tauri.annotation.Command
import app.tauri.annotation.InvokeArg
import app.tauri.annotation.TauriPlugin

@InvokeArg
internal class OpenAppArgs {
  lateinit var name: String
  var timeout: Int? = null
}

@InvokeArg
internal class OpenArgs {
  lateinit var requiredArg: String
  var allowEdit: Boolean = false
  var quality: Int = 100
  var app: OpenAppArgs? = null
}

@TauriPlugin
class ExamplePlugin(private val activity: Activity): Plugin(activity) {
  @Command
  fun openCamera(invoke: Invoke) {
    val args = invoke.parseArgs(OpenArgs::class.java)
  }
}
```

{{% alert title="注意" %}}
可选参数定义为 `var <argumentName>: Type? = null`。

带默认值的参数定义为 `var <argumentName>: Type = <default-value>`。

必需参数定义为 `lateinit var <argumentName>: Type`。
{{% /alert %}}

### iOS

在 iOS 上，参数被定义为继承 `Decodable` 的类。内部对象也必须继承 Decodable 协议：

```swift
class OpenAppArgs: Decodable {
  let name: String
  var timeout: Int?
}

class OpenArgs: Decodable {
  let requiredArg: String
  var allowEdit: Bool?
  var quality: UInt8?
  var app: OpenAppArgs?
}

class ExamplePlugin: Plugin {
	@objc public func openCamera(_ invoke: Invoke) throws {
    let args = try invoke.parseArgs(OpenArgs.self)

    invoke.resolve(["path": "/path/to/photo.jpg"])
	}
}
```

{{% alert title="注意" %}}
可选参数定义为 `var <argumentName>: Type?`。

带默认值的参数**不**受支持。
请使用可空类型，并在命令函数中设置默认值。

必需参数定义为 `let <argumentName>: Type`。
{{% /alert %}}

## 从移动端插件调用 Rust

出于性能和可复用性的考虑，把插件代码写在 Rust 中往往更可取。虽然 Tauri 不直接提供从插件代码调用 Rust 的机制，但在 Android 上使用 JNI、在 iOS 上使用 FFI 可以让插件调用共享代码，即使应用 WebView 处于挂起状态也可以。

### Android

在插件的 `Cargo.toml` 中把 jni crate 添加为依赖：

```toml
jni = "0.21"
```

静态加载应用库，并在 Kotlin 代码中定义 native 函数。在本例中，Kotlin 类是 `com.example.HelloWorld`，我们需要从 Rust 侧引用完整的包名。

```kotlin

init {
  try {
    // 加载原生库（libapp_lib.so）
    // 这是 Cargo 以 crate-type = ["cdylib"] 构建出的共享库
    System.loadLibrary("app_lib")
    Log.d(TAG, "Successfully loaded libapp_lib.so")
  } catch (e: UnsatisfiedLinkError) {
    Log.e(TAG, "Failed to load libapp_lib.so", e)
    throw e
  }
}

external fun helloWorld(name: String): String?
```

然后在插件的 Rust 代码中定义 JNI 要查找的函数。函数格式为 `Java_package_class_method`，因此对于上面这个类，它会变成 `Java_com_example_HelloWorld_helloWorld`，从而被我们的 `helloWorld` 方法调用：

```rust
#[no_mangle]
pub extern "system" fn Java_com_example_HelloWorld_helloWorld(
    mut env: JNIEnv,
    _class: JClass,
    name: JString,
) -> jstring {
    log::debug!("Calling JNI Hello World!");
    let result = format!("Hello, {}!", name);

    match env.new_string(result) {
        Ok(jstr) => jstr.into_raw(),
        Err(e) => {
            log::error!("Failed to create JString: {}", e);
            std::ptr::null_mut()
        }
    }
}
```

### iOS

iOS 只使用标准的 C FFI，因此不需要任何新依赖。在你的 Swift 代码中加入钩子以及必要的清理。这些函数可以取任何合法名称，但必须用 `@_silgen_name(FFI_FUNC)` 注解，其中 FFI_FUNC 是要从 Rust 调用的函数名：

```swift
private static func helloWorldFFI(_ name: UnsafePointer<CChar>) -> UnsafeMutablePointer<CChar>?

@_silgen_name("free_hello_result_ffi")
private static func freeHelloResult(_ result: UnsafeMutablePointer<CChar>)

static func helloWorld(name: String) -> String? {
  // 调用 Rust FFI
  let resultPtr = name.withCString({ helloWorldFFI($0) })

  // 把 C 字符串转换为 Swift String
  let result = String(cString: resultPtr)

  // 释放 C 字符串
  freeHelloResult(resultPtr)

  return result
}

```

然后实现 Rust 侧。这里的 `extern` 函数必须与 Swift 侧的 `@_silgen_name` 注解一致：

```rust
pub unsafe extern "C" fn hello_world_ffi(c_name: *const c_char) -> *mut c_char {
    let name = match CStr::from_ptr(c_name).to_str() {
        Ok(s) => s,
        Err(e) => {
            log::error!("[iOS FFI] Failed to convert C string: {}", e);
            return std::ptr::null_mut();
        }
    };

    let result = format!("Hello, {}!", name);

    match CString::new(result) {
        Ok(c_str) => c_str.into_raw(),
        Err(e) => {
            log::error!("[iOS FFI] Failed to create C string: {}", e);
            std::ptr::null_mut()
        }
    }
}

#[no_mangle]
pub unsafe extern "C" fn free_hello_result_ffi(result: *mut c_char) {
    if !result.is_null() {
        drop(CString::from_raw(result));
    }
}
```

## Android 16KB 内存页

Google 正在推动把所有新提交的 Android 应用都要求使用 16KB 内存页。使用 NDK 28 或更高版本构建应当会自动生成满足该要求的打包产物，但如果必须使用更旧的 NDK 版本，或者生成的文件没有按 16KB 对齐，可以在 `.cargo/config.toml` 中加入以下内容来向 `rustc` 标明这一点：

```toml
rustflags = ["-C", "link-arg=-Wl,-z,max-page-size=16384"]
```

## 权限

如果插件需要终端用户授予权限，Tauri 简化了检查与请求权限的过程。

**移动端操作系统**

{{< tabpane text=true persist=disabled >}}
{{% tab header="Android" %}}

首先定义所需权限的列表，以及用于在代码中标识每个组的别名。这在 `TauriPlugin` 注解中完成：

```kotlin
  permissions = [
    Permission(strings = [Manifest.permission.POST_NOTIFICATIONS], alias = "postNotification")
  ]
)
class ExamplePlugin(private val activity: Activity): Plugin(activity) { }
```

{{% /tab %}}

{{% tab header="iOS" %}}

首先重写 `checkPermissions` 和 `requestPermissions` 函数：

```swift
class ExamplePlugin: Plugin {
  @objc open func checkPermissions(_ invoke: Invoke) {
    invoke.resolve(["postNotification": "prompt"])
  }

  @objc public override func requestPermissions(_ invoke: Invoke) {
    // 在这里请求权限
    // 然后兑现该请求
    invoke.resolve(["postNotification": "granted"])
  }
}
```

{{% /tab %}}

{{< /tabpane >}}
Tauri 会自动为该插件实现两个命令：`checkPermissions` 和 `requestPermissions`。
这些命令可以直接从 JavaScript 或 Rust 调用：

**语言**

{{< tabpane text=true persist=disabled >}}
{{% tab header="JavaScript" %}}

```javascript
import { invoke, PermissionState } from '@tauri-apps/api/core'

interface Permissions {
  postNotification: PermissionState
}

// 检查权限状态
const permission = await invoke<Permissions>('plugin:<plugin-name>|checkPermissions')

if (permission.postNotification === 'prompt-with-rationale') {
  // 向用户说明为什么需要该权限
}

// 请求权限
if (permission.postNotification.startsWith('prompt')) {
  const state = await invoke<Permissions>('plugin:<plugin-name>|requestPermissions', { permissions: ['postNotification'] })
}
```

{{% /tab %}}

{{% tab header="Rust" %}}

```rust
use serde::{Serialize, Deserialize};
use tauri::{plugin::PermissionState, Runtime};

#[derive(Deserialize)]
#[serde(rename_all = "camelCase")]
struct PermissionResponse {
  pub post_notification: PermissionState,
}

#[derive(Serialize)]
#[serde(rename_all = "camelCase")]
struct RequestPermission {
  post_notification: bool,
}

impl<R: Runtime> Notification<R> {
  pub fn request_post_notification_permission(&self) -> crate::Result<PermissionState> {
    self.0
      .run_mobile_plugin::<PermissionResponse>("requestPermissions", RequestPermission { post_notification: true })
      .map(|r| r.post_notification)
      .map_err(Into::into)
  }

  pub fn check_permissions(&self) -> crate::Result<PermissionResponse> {
    self.0
      .run_mobile_plugin::<PermissionResponse>("checkPermissions", ())
      .map_err(Into::into)
  }
}
```

{{% /tab %}}

{{< /tabpane >}}
## 插件事件

插件可以在任何时候使用 `trigger` 函数发出事件：

**移动端操作系统**

{{< tabpane text=true persist=disabled >}}
{{% tab header="Android" %}}

```kotlin
class ExamplePlugin(private val activity: Activity): Plugin(activity) {
    override fun load(webView: WebView) {
      trigger("load", JSObject())
    }

    override fun onNewIntent(intent: Intent) {
      // 处理新的 intent 事件
      if (intent.action == Intent.ACTION_VIEW) {
        val data = intent.data.toString()
        val event = JSObject()
        event.put("data", data)
        trigger("newIntent", event)
      }
    }

    @Command
    fun openCamera(invoke: Invoke) {
      val payload = JSObject()
      payload.put("open", true)
      trigger("camera", payload)
    }
}
```

{{% /tab %}}

{{% tab header="iOS" %}}

```swift
class ExamplePlugin: Plugin {
  @objc public override func load(webview: WKWebView) {
    trigger("load", data: [:])
  }

  @objc public func openCamera(_ invoke: Invoke) {
    trigger("camera", data: ["open": true])
  }
}
```

{{% /tab %}}

{{< /tabpane >}}
之后可以在 NPM 包中使用 [`addPluginListener`](https://tauri.app/reference/javascript/api/namespacecore/#addpluginlistener) 辅助函数调用这些辅助函数：

```javascript
import { addPluginListener, PluginListener } from '@tauri-apps/api/core';

export async function onRequest(
	handler: (url: string) => void
): Promise<PluginListener> {
	return await addPluginListener(
		'<plugin-name>',
		'event-name',
		handler
	);
}
```

{{% alert title="需要能力" %}}

从 JavaScript 监听插件事件，受与插件命令相同的[能力](../../../security/4-capabilities/)和[权限](../../../security/2-permissions/)系统管控。请把该插件的权限（通常是 `<plugin-name>:default`，如果插件定义了特定的 `allow-listen-*` 权限则用它）加入 `src-tauri/capabilities/` 下某个能力的 `permissions` 数组：

```json
{
  "identifier": "default",
  "windows": ["main"],
  "permissions": ["<plugin-name>:default"]
}
```

它具体暴露哪些权限标识符，请参阅插件自身的文档。

{{% /alert %}}
