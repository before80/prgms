+++
title = "3 从前端调用 Rust"
date = 2026-09-25T21:31:08+08:00
weight = 3
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/develop/calling-rust/](https://tauri.app/develop/calling-rust/)

本文档介绍如何从应用前端与 Rust 代码通信。
如果想了解如何从 Rust 代码与前端通信，请参阅[从 Rust 调用前端](../4-callingfrontend/)。

Tauri 提供了带类型安全的、用于调用 Rust 函数的[命令](#命令)原语，以及更动态的[事件系统](#事件系统)。

## 命令

Tauri 提供了一套简单而强大的 `command` 系统，用于从 Web 应用调用 Rust 函数。
命令可以接收参数并返回值，也可以返回错误，还可以是 `async` 的。

### 基本示例

命令可以定义在 `src-tauri/src/lib.rs` 文件中。
要创建命令，只需添加一个函数并加上 `#[tauri::command]` 注解：

```rust
fn my_custom_command() {
	println!("I was invoked from JavaScript!");
}
```

{{% alert title="注意" %}}
命令名必须唯一。
{{% /alert %}}

{{% alert title="注意" %}}
由于胶水代码生成的限制，定义在 `lib.rs` 文件中的命令不能被标记为 `pub`。
如果你把它标记为公开函数，会看到类似这样的错误：

```
error[E0255]: the name `__cmd__command_name` is defined multiple times
  --> src/lib.rs:28:8
   |
27 | #[tauri::command]
   | ----------------- previous definition of the macro `__cmd__command_name` here
28 | pub fn x() {}
   |        ^ `__cmd__command_name` reimported here
   |
   = note: `__cmd__command_name` must be defined only once in the macro namespace of this module
```

{{% /alert %}}

你还需要把你的命令列表提供给 builder 函数，如下所示：

```rust
pub fn run() {
	tauri::Builder::default()
		.invoke_handler(tauri::generate_handler![my_custom_command])
		.run(tauri::generate_context!())
		.expect("error while running tauri application");
}
```

现在，你可以在 JavaScript 代码中调用该命令：

```javascript
import { invoke } from '@tauri-apps/api/core';

// 使用 Tauri 全局脚本时（不使用 npm 包）
// 请确保在 `tauri.conf.json` 中把 `app.withGlobalTauri` 设为 true
const invoke = window.__TAURI__.core.invoke;

// 调用命令
invoke('my_custom_command');
```

#### 在独立模块中定义命令

如果你的应用定义了很多组件，或者它们可以分组，你可以把命令定义在独立模块中，而不是让 `lib.rs` 文件变得臃肿。

举例来说，我们在 `src-tauri/src/commands.rs` 文件中定义一个命令：

```rust
pub fn my_custom_command() {
	println!("I was invoked from JavaScript!");
}
```

{{% alert title="注意" %}}
在独立模块中定义命令时，它们应当被标记为 `pub`。
{{% /alert %}}

{{% alert title="注意" %}}
命令名不按模块划分作用域，因此即使在不同模块之间，命令名也必须唯一。
{{% /alert %}}

在 `lib.rs` 文件中声明该模块，并相应地提供命令列表：

```rust

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
	tauri::Builder::default()
		.invoke_handler(tauri::generate_handler![commands::my_custom_command])
		.run(tauri::generate_context!())
		.expect("error while running tauri application");
}
```

注意命令列表中的 `commands::` 前缀，它表示命令函数的完整路径。

这个示例中的命令名是 `my_custom_command`，因此你在前端仍然可以通过执行 `invoke("my_custom_command")` 来调用它，`commands::` 前缀会被忽略。

#### WASM

当使用 Rust 前端调用不带参数的 `invoke()` 时，你需要按下面这样调整前端代码。
原因是 Rust 不支持可选参数。

```rust
extern "C" {
    // 不带参数调用
    #[wasm_bindgen(js_namespace = ["window", "__TAURI__", "core"], js_name = invoke)]
    async fn invoke_without_args(cmd: &str) -> JsValue;

    // 带参数调用（默认）
    #[wasm_bindgen(js_namespace = ["window", "__TAURI__", "core"])]
    async fn invoke(cmd: &str, args: JsValue) -> JsValue;

    // 它们必须使用不同的名称！
}
```

### 传递参数

你的命令处理函数可以接收参数：

```rust
fn my_custom_command(invoke_message: String) {
	println!("I was invoked from JavaScript, with this message: {}", invoke_message);
}
```

参数应当以 camelCase 键的 JSON 对象传入：

```javascript
invoke('my_custom_command', { invokeMessage: 'Hello!' });
```

{{% alert title="注意" %}}
你可以用 `rename_all` 属性让参数使用 `snake_case`：

```rust
fn my_custom_command(invoke_message: String) {}
```

对应的 JavaScript：

```javascript
invoke('my_custom_command', { invoke_message: 'Hello!' });
```

{{% /alert %}}

参数可以是任意类型，只要它实现了 [`serde::Deserialize`](https://docs.serde.rs/serde/trait.Deserialize.html)。

### 返回数据

命令处理函数也可以返回数据：

```rust
fn my_custom_command() -> String {
	"Hello from Rust!".into()
}
```

`invoke` 函数返回一个 promise，它会以返回值兑现：

```javascript
#[tauri::command]
fn my_custom_command() -> String {
	"Hello from Rust!".into()
}
```

返回的数据可以是任意类型，只要它实现了 [`serde::Serialize`](https://docs.serde.rs/serde/trait.Serialize.html)。

#### 返回 ArrayBuffer

实现了 [`serde::Serialize`](https://docs.serde.rs/serde/trait.Serialize.html) 的返回值在响应发送给前端时会被序列化为 JSON。
如果你尝试返回文件或下载的 HTTP 响应之类的大数据，这会拖慢应用。
要以优化的方式返回 array buffer，请使用 [`tauri::ipc::Response`](https://docs.rs/tauri/2.0.0/tauri/ipc/struct.Response.html)：

```rust
#[tauri::command]
fn read_file() -> Response {
	let data = std::fs::read("/path/to/file").unwrap();
	tauri::ipc::Response::new(data)
}
```

### 错误处理

如果你的处理函数可能失败并需要返回错误，让函数返回 `Result`：

```rust
fn login(user: String, password: String) -> Result<String, String> {
	if user == "tauri" && password == "tauri" {
		// 成功
		Ok("logged_in".to_string())
	} else {
		// 失败
		Err("invalid credentials".to_string())
	}
}
```

如果命令返回错误，promise 会被拒绝，否则会被兑现：

```javascript
invoke('login', { user: 'tauri', password: '0j4rijw8=' })
  .then((message) => console.log(message))
  .catch((error) => console.error(error));
```

如前所述，命令返回的所有内容（包括错误）都必须实现 [`serde::Serialize`](https://docs.serde.rs/serde/trait.Serialize.html)。
如果你要处理 Rust 标准库或外部 crate 的错误类型，这可能会有问题，因为大多数错误类型都没有实现它。
在简单的场景中，你可以用 `map_err` 把这些错误转换成 `String`：

```rust
fn my_custom_command() -> Result<(), String> {
	std::fs::File::open("path/to/file").map_err(|err| err.to_string())?;
	// 成功时返回 `null`
	Ok(())
}
```

由于这不太符合习惯用法，你可能想创建自己的错误类型并实现 `serde::Serialize`。
在下面的示例中，我们使用 [`thiserror`](https://github.com/dtolnay/thiserror) crate 来帮助创建错误类型。
它允许你通过派生 `thiserror::Error` trait 把枚举变成错误类型。
更多细节可以查阅它的文档。

```rust
#[derive(Debug, thiserror::Error)]
enum Error {
	#[error(transparent)]
	Io(#[from] std::io::Error)
}

// 我们必须手动实现 serde::Serialize
impl serde::Serialize for Error {
	fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
	where
		S: serde::ser::Serializer,
	{
		serializer.serialize_str(self.to_string().as_ref())
	}
}

#[tauri::command]
fn my_custom_command() -> Result<(), Error> {
	// 这会返回一个错误
	std::fs::File::open("path/that/does/not/exist")?;
	// 成功时返回 `null`
	Ok(())
}
```

自定义错误类型的优势在于：它把所有可能的错误都显式化，读者可以快速看出可能发生哪些错误。
这能为别人（以及你自己）日后审查和重构代码节省大量时间。<br/>
它还让你完全掌控错误类型的序列化方式。
在上面的示例中，我们只是把错误信息作为字符串返回，但你也可以给每个错误分配一个错误码，
这样就能更容易地把它映射到外观相似的 TypeScript 错误枚举，例如：

```rust
enum Error {
  #[error(transparent)]
  Io(#[from] std::io::Error),
  #[error("failed to parse as string: {0}")]
  Utf8(#[from] std::str::Utf8Error),
}

#[derive(serde::Serialize)]
#[serde(tag = "kind", content = "message")]
#[serde(rename_all = "camelCase")]
enum ErrorKind {
  Io(String),
  Utf8(String),
}

impl serde::Serialize for Error {
  fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
  where
    S: serde::ser::Serializer,
  {
    let error_message = self.to_string();
    let error_kind = match self {
      Self::Io(_) => ErrorKind::Io(error_message),
      Self::Utf8(_) => ErrorKind::Utf8(error_message),
    };
    error_kind.serialize(serializer)
  }
}

#[tauri::command]
fn read() -> Result<Vec<u8>, Error> {
  let data = std::fs::read("/path/to/file")?;
	Ok(data)
}
```

现在你在前端会得到 `{ kind: 'io' | 'utf8', message: string }` 这样的错误对象：

```ts
type ErrorKind = {
  kind: 'io' | 'utf8';
  message: string;
};

invoke('read').catch((e: ErrorKind) => {});
```

### 异步命令

在 Tauri 中，执行繁重工作时更推荐使用异步命令，这样不会造成 UI 卡顿或变慢。

{{% alert title="注意" %}}

异步命令会通过 [`async_runtime::spawn`](https://docs.rs/tauri/2.0.0/tauri/async_runtime/fn.spawn.html) 在独立的异步任务上执行。
不带 _async_ 关键字的命令在主线程上执行，除非用 _#[tauri::command(async)]_ 定义。

{{% /alert %}}

**如果你的命令需要异步运行，只需把它声明为 `async`。**

{{% alert title="警告" color="warning" %}}

使用 Tauri 创建异步函数时需要小心。
目前你不能在异步函数签名中直接包含借用型参数。
这类类型的常见例子有 `&str` 和 `State<'_, Data>`。
该限制跟踪于：https://github.com/tauri-apps/tauri/issues/2533 ，变通方法见下文。

{{% /alert %}}

处理借用类型时，你必须做额外改动。主要有两个选项：

**选项 1**：把类型转换成不借用的相似类型，例如把 `&str` 换成 `String`。
这可能不适用于所有类型，例如 `State<'_, Data>`。

_示例：_

```rust
#[tauri::command]
async fn my_custom_command(value: String) -> String {
	// 调用另一个异步函数并等待它完成
	some_async_function().await;
	value
}
```

**选项 2**：把返回类型包进 [`Result`](https://doc.rust-lang.org/std/result/index.html)。这个稍难实现，但适用于所有类型。

使用 `Result<a, b>` 作为返回类型，把 `a` 替换为你希望返回的类型（如果想返回 `null` 就用 `()`），把 `b` 替换为出错时要返回的错误类型（如果不想返回可选错误就用 `()`）。例如：

- `Result<String, ()>` 返回 String，且不返回错误。
- `Result<(), ()>` 返回 `null`。
- `Result<bool, Error>` 返回布尔值或错误，如上面的[错误处理](#错误处理)一节所示。

_示例：_

```rust
#[tauri::command]
async fn my_custom_command(value: &str) -> Result<String, ()> {
	// 调用另一个异步函数并等待它完成
	some_async_function().await;
	// 注意返回值现在必须包在 `Ok()` 中。
	Ok(format!(value))
}
```

##### 从 JavaScript 调用

由于从 JavaScript 调用命令本来就返回 promise，它的用法与其它命令完全一样：

```javascript
invoke('my_custom_command', { value: 'Hello, Async!' }).then(() =>
  console.log('Completed!')
);
```

### 通道

Tauri 的通道（channel）是把流式 HTTP 响应之类的数据流式传输到前端的推荐机制。
下面的示例读取一个文件，并按 4096 字节的分块把进度通知给前端：

```rust

#[tauri::command]
async fn load_image(path: std::path::PathBuf, reader: tauri::ipc::Channel<&[u8]>) {
  // 为简单起见，这个示例没有包含错误处理
  let mut file = tokio::fs::File::open(path).await.unwrap();

  let mut chunk = vec![0; 4096];

  loop {
    let len = file.read(&mut chunk).await.unwrap();
    if len == 0 {
      // 长度为 0 表示文件结束。
      break;
    }
    reader.send(&chunk).unwrap();
  }
}
```

更多信息请参阅[通道文档](../4-callingfrontend/#通道)。

### 在命令中访问 WebviewWindow

命令可以访问调用该消息的 `WebviewWindow` 实例：

```rust
async fn my_custom_command(webview_window: tauri::WebviewWindow) {
	println!("WebviewWindow: {}", webview_window.label());
}
```

### 在命令中访问 AppHandle

命令可以访问 `AppHandle` 实例：

```rust
async fn my_custom_command(app_handle: tauri::AppHandle) {
	let app_dir = app_handle.path().app_dir();
	use tauri::GlobalShortcutManager;
	app_handle.global_shortcut_manager().register("CTRL + U", move || {});
}
```

{{% alert title="提示" %}}

`AppHandle` 和 `WebviewWindow` 都带有一个泛型参数 `R: Runtime`。
当 `tauri` 启用了 `wry` 特性时（默认启用），我们把该泛型默认设为 `Wry` 运行时，因此你可以直接使用它们；
但如果你想使用其它运行时，例如 [mock 运行时](https://docs.rs/tauri/2.0.0/tauri/test/struct.MockRuntime.html)，就需要这样写你的函数：

```rust
use tauri::{AppHandle, GlobalShortcutManager, Runtime, WebviewWindow};

#[tauri::command]
async fn my_custom_command<R: Runtime>(app_handle: AppHandle<R>, webview_window: WebviewWindow<R>) {
  let app_dir = app_handle.path().app_dir();
  app_handle
    .global_shortcut_manager()
    .register("CTRL + U", move || {});
  println!("WebviewWindow: {}", webview_window.label());
}
```

{{% /alert %}}

### 访问托管的 state

Tauri 可以使用 `tauri::Builder` 上的 `manage` 函数来管理 state。
在命令中可以通过 `tauri::State` 访问该 state：

```rust

#[tauri::command]
fn my_custom_command(state: tauri::State<MyState>) {
	assert_eq!(state.0 == "some state value", true);
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
	tauri::Builder::default()
		.manage(MyState("some state value".into()))
		.invoke_handler(tauri::generate_handler![my_custom_command])
		.run(tauri::generate_context!())
		.expect("error while running tauri application");
}
```

### 访问原始请求

Tauri 命令还可以访问完整的 [`tauri::ipc::Request`](https://docs.rs/tauri/2.0.0/tauri/ipc/struct.Request.html) 对象，其中包含原始请求体负载和请求头。

```rust
enum Error {
  #[error("unexpected request body")]
  RequestBodyMustBeRaw,
  #[error("missing `{0}` header")]
  MissingHeader(&'static str),
}

impl serde::Serialize for Error {
  fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
  where
    S: serde::ser::Serializer,
  {
    serializer.serialize_str(self.to_string().as_ref())
  }
}

#[tauri::command]
fn upload(request: tauri::ipc::Request) -> Result<(), Error> {
  let tauri::ipc::InvokeBody::Raw(upload_data) = request.body() else {
    return Err(Error::RequestBodyMustBeRaw);
  };
  let Some(authorization_header) = request.headers().get("Authorization") else {
    return Err(Error::MissingHeader("Authorization"));
  };

  // 上传……

  Ok(())
}
```

在前端，你可以通过在 payload 参数中提供 ArrayBuffer 或 Uint8Array 来调用 invoke() 发送原始请求体，
并在第三个参数中包含请求头：

```js
await __TAURI__.core.invoke('upload', data, {
  headers: {
    Authorization: 'apikey',
  },
});
```

### 创建多个命令

`tauri::generate_handler!` 宏接收一个命令数组。要注册
多个命令，你不能多次调用 invoke_handler。只有最后一次调用会生效。
你必须把每个命令都传给 `tauri::generate_handler!` 的单次调用。

```rust
fn cmd_a() -> String {
	"Command a"
}
#[tauri::command]
fn cmd_b() -> String {
	"Command b"
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
	tauri::Builder::default()
		.invoke_handler(tauri::generate_handler![cmd_a, cmd_b])
		.run(tauri::generate_context!())
		.expect("error while running tauri application");
}
```

### 完整示例

上述特性中的任意一个或全部都可以组合使用：

```rust

#[derive(serde::Serialize)]
struct CustomResponse {
	message: String,
	other_val: usize,
}

async fn some_other_function() -> Option<String> {
	Some("response".into())
}

#[tauri::command]
async fn my_custom_command(
	window: tauri::WebviewWindow,
	number: usize,
	database: tauri::State<'_, Database>,
) -> Result<CustomResponse, String> {
	println!("Called from {}", window.label());
	let result: Option<String> = some_other_function().await;
	if let Some(message) = result {
		Ok(CustomResponse {
			message,
			other_val: 42 + number,
		})
	} else {
		Err("No result".into())
	}
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
	tauri::Builder::default()
		.manage(Database {})
		.invoke_handler(tauri::generate_handler![my_custom_command])
		.run(tauri::generate_context!())
		.expect("error while running tauri application");
}
```

```javascript
import { invoke } from '@tauri-apps/api/core';

// 从 JavaScript 调用
invoke('my_custom_command', {
  number: 42,
})
  .then((res) =>
    console.log(`Message: ${res.message}, Other Val: ${res.other_val}`)
  )
  .catch((e) => console.error(e));
```

## 事件系统

事件系统是前端与 Rust 之间更简单的通信机制。
与命令不同，事件不是类型安全的，始终是异步的，不能返回值，且只支持 JSON 负载。

### 全局事件

要触发全局事件，你可以使用 [event.emit](https://tauri.app/reference/javascript/api/namespaceevent/#emit) 或 [WebviewWindow#emit](https://tauri.app/reference/javascript/api/namespacewebviewwindow/#emit) 函数：

```js
import { emit } from '@tauri-apps/api/event';
import { getCurrentWebviewWindow } from '@tauri-apps/api/webviewWindow';

// emit(eventName, payload)
emit('file-selected', '/path/to/file');

const appWebview = getCurrentWebviewWindow();
appWebview.emit('route-changed', { url: window.location.href });
```

{{% alert title="注意" %}}
全局事件会投递给**所有**监听器
{{% /alert %}}

### Webview 事件

要触发事件给某个特定 webview 注册的监听器，你可以使用 [event.emitTo](https://tauri.app/reference/javascript/api/namespaceevent/#emitto) 或 [WebviewWindow#emitTo](https://tauri.app/reference/javascript/api/namespacewebviewwindow/#emitto) 函数：

```js
import { emitTo } from '@tauri-apps/api/event';
import { getCurrentWebviewWindow } from '@tauri-apps/api/webviewWindow';

// emitTo(webviewLabel, eventName, payload)
emitTo('settings', 'settings-update-requested', {
  key: 'notification',
  value: 'all',
});

const appWebview = getCurrentWebviewWindow();
appWebview.emitTo('editor', 'file-changed', {
  path: '/path/to/file',
  contents: 'file contents',
});
```

{{% alert title="注意" %}}
Webview 特定的事件**不会**触发给普通的全局事件监听器。
要监听**任意**事件，你必须给 [event.listen](https://tauri.app/reference/javascript/api/namespaceevent/#listen) 函数提供 `{ target: { kind: 'Any' } }` 选项，它会让该监听器成为所有已发出事件的兜底监听器：

```js
import { listen } from '@tauri-apps/api/event';
listen(
  'state-changed',
  (event) => {
    console.log('got state changed event', event);
  },
  {
    target: { kind: 'Any' },
  }
);
```

{{% /alert %}}

### 监听事件

`@tauri-apps/api` NPM 包提供了监听全局事件和 webview 特定事件的 API。

- 监听全局事件

  ```ts
  import { listen } from '@tauri-apps/api/event';

  type DownloadStarted = {
    url: string;
    downloadId: number;
    contentLength: number;
  };

  listen<DownloadStarted>('download-started', (event) => {
    console.log(
      `downloading ${event.payload.contentLength} bytes from ${event.payload.url}`
    );
  });
  ```

- 监听 webview 特定事件

  ```ts
  import { getCurrentWebviewWindow } from '@tauri-apps/api/webviewWindow';

  const appWebview = getCurrentWebviewWindow();
  appWebview.listen<string>('logged-in', (event) => {
    localStorage.setItem('session-token', event.payload);
  });
  ```

`listen` 函数会让事件监听器在整个应用生命周期内保持注册。
要停止监听某个事件，你可以使用 `listen` 函数返回的 `unlisten` 函数：

```js
import { listen } from '@tauri-apps/api/event';

const unlisten = await listen('download-started', (event) => {});
unlisten();
```

{{% alert title="注意" %}}
当你的执行上下文离开作用域时（例如组件被卸载），一定要调用 unlisten 函数。

当页面重新加载或你导航到另一个 URL 时，监听器会自动注销。
但这不适用于单页应用（SPA）路由。
{{% /alert %}}

#### 常见陷阱

##### 不要在监听器兑现之前调用 `unlisten()`

`listen` 函数返回一个 Promise，它会兑现为 `unlisten` 句柄。
如果你在 Promise 兑现之前同步调用 `unlisten`，处理函数会立即被移除，你将收不到任何事件：

```js
const unlisten = listen('sync-complete', (event) => {
  console.log('sync finished');
});
unlisten(); // 这里的 unlisten 是 Promise，不是函数——监听器不会被清理

// 正确：await 这个 Promise 以获得 unlisten 句柄
const unlisten = await listen('sync-complete', (event) => {
  console.log('sync finished');
});
// 现在你可以保存它并在之后调用，例如在清理函数中
unlisten();
```

##### setup 钩子中的时序问题

在 React、Vue、Svelte 等框架中，setup 或 mount 钩子在组件完全渲染之前就会运行。如果你在 setup 期间监听事件，请确保事件处理函数不依赖尚未渲染的 DOM 元素，或者把监听器的注册推迟到 mount 之后运行的 effect/hook 中。

```js
function MyComponent() {
  const ref = useRef(null);
  listen('scroll-to', (event) => {
    ref.current.scrollIntoView(); // setup 期间 ref.current 可能为 null
  });
  return <div ref={ref} />;
}

// 正确：使用在组件挂载后运行的 useEffect
function MyComponent() {
  const ref = useRef(null);
  useEffect(() => {
    const unlisten = listen('scroll-to', (event) => {
      ref.current?.scrollIntoView();
    });
    return () => {
      unlisten.then((fn) => fn());
    };
  }, []);
  return <div ref={ref} />;
}
```

##### 事件顺序与异步监听器

事件监听器按注册顺序调用，但如果某个监听器是异步的，而事件发送方快速连续发送多个事件，监听器处理事件的顺序就可能错乱。对于需要保序的高吞吐数据投递，请考虑使用[通道](../4-callingfrontend/#通道)而不是事件系统。

#### 各框架的清理示例

使用前端框架时，你应该在组件卸载时清理事件监听器，以避免内存泄漏和重复的处理函数。

**框架**

{{< tabpane text=true persist=disabled >}}
{{% tab header="React" %}}

```tsx
import { useEffect, useState } from 'react';
import { listen } from '@tauri-apps/api/event';

function DownloadTracker() {
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    const unlisten = listen<number>('download-progress', (event) => {
      setProgress(event.payload);
    });

    return () => {
      unlisten.then((fn) => fn());
    };
  }, []);

  return <div>Download progress: {progress}%</div>;
}
```

{{% /tab %}}

{{% tab header="Vue" %}}

```vue
import { ref, onMounted, onUnmounted } from 'vue';
import { listen } from '@tauri-apps/api/event';

const progress = ref(0);
let unlistenPromise;

onMounted(() => {
  unlistenPromise = listen<number>('download-progress', (event) => {
    progress.value = event.payload;
  });
});

onUnmounted(() => {
  unlistenPromise?.then((fn) => fn());
});
</script>

<template>
  <div>Download progress: {{ progress }}%</div>
</template>
```

{{% /tab %}}

{{% tab header="Svelte" %}}

```svelte
import { listen } from '@tauri-apps/api/event';

let progress = $state(0);

$effect(() => {
  const unlistenPromise = listen<number>(
    'download-progress',
    (event) => {
      progress = event.payload;
    }
  );

  return () => {
    unlistenPromise.then((unlisten) => unlisten());
  };
});
</script>

<div>Download progress: {progress}%</div>
```

{{% /tab %}}

{{< /tabpane >}}
此外，Tauri 还提供了一个只监听一次事件的工具函数：

```js
import { once } from '@tauri-apps/api/event';
import { getCurrentWebviewWindow } from '@tauri-apps/api/webviewWindow';

once('ready', (event) => {});

const appWebview = getCurrentWebviewWindow();
appWebview.once('ready', () => {});
```

{{% alert title="注意" %}}
前端发出的事件也会触发通过这些 API 注册的监听器。
更多信息请参阅[从前端调用 Rust](../4-callingfrontend/)文档。
{{% /alert %}}

#### 在 Rust 中监听事件

全局事件和 webview 特定事件也会投递给在 Rust 中注册的监听器。

- 监听全局事件

  ```rust
  use tauri::Listener;

  #[cfg_attr(mobile, tauri::mobile_entry_point)]
  pub fn run() {
    tauri::Builder::default()
      .setup(|app| {
        app.listen("download-started", |event| {
          if let Ok(payload) = serde_json::from_str::<DownloadStarted>(&event.payload()) {
            println!("downloading {}", payload.url);
          }
        });
        Ok(())
      })
      .run(tauri::generate_context!())
      .expect("error while running tauri application");
  }
  ```

- 监听 webview 特定事件

  ```rust
  use tauri::{Listener, Manager};

  #[cfg_attr(mobile, tauri::mobile_entry_point)]
  pub fn run() {
    tauri::Builder::default()
      .setup(|app| {
        let webview = app.get_webview_window("main").unwrap();
        webview.listen("logged-in", |event| {
          let session_token = event.data;
          // 保存 token……
        });
        Ok(())
      })
      .run(tauri::generate_context!())
      .expect("error while running tauri application");
  }
  ```

`listen` 函数会让事件监听器在整个应用生命周期内保持注册。
要停止监听某个事件，你可以使用 `unlisten` 函数：

```rust
let event_id = app.listen("download-started", |event| {});
app.unlisten(event_id);

// 在满足某些事件条件时 unlisten
let handle = app.handle().clone();
app.listen("status-changed", |event| {
  if event.data == "ready" {
    handle.unlisten(event.id);
  }
});
```

此外，Tauri 还提供了一个只监听一次事件的工具函数：

```rust
app.once("ready", |event| {
  println!("app is ready");
});
```

在这种情况下，事件监听器在第一次触发后会立即注销。

如果想了解如何从 Rust 代码监听事件和发出事件，请参阅 [Rust 事件系统文档](../4-callingfrontend/#事件系统)。
