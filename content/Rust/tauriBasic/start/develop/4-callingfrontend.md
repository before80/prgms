+++
title = "4 从 Rust 调用前端"
date = 2026-09-25T21:31:08+08:00
weight = 4
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/develop/calling-frontend/](https://tauri.app/develop/calling-frontend/)

本文档介绍如何从 Rust 代码与应用前端通信。
如果想了解如何从前端与 Rust 代码通信，请参阅[从前端调用 Rust](../3-callingrust/)。

Tauri 应用的 Rust 侧可以通过 Tauri 事件系统调用前端，也可以使用通道，或直接执行 JavaScript 代码。

## 事件系统

Tauri 提供了一套简单的事件系统，让你可以在 Rust 与前端之间进行双向通信。

事件系统是为需要流式传输少量数据，或需要实现多消费者多生产者模式（例如推送通知系统）的场景设计的。

事件系统并非为低延迟或高吞吐场景设计。
流式数据请参阅针对其优化的[通道一节](#通道)。

Tauri 命令与 Tauri 事件的主要区别在于：事件没有强类型支持，
事件负载始终是 JSON 字符串，因此不适合较大的消息，
并且不支持用[能力](../../security/4-capabilities/)系统对事件数据与通道做细粒度控制。

[AppHandle](https://docs.rs/tauri/2.0.0/tauri/struct.AppHandle.html) 和 [WebviewWindow](https://docs.rs/tauri/2.0.0/tauri/webview/struct.WebviewWindow.html) 类型实现了事件系统 trait [Listener](https://docs.rs/tauri/2.0.0/tauri/trait.Listener.html) 和 [Emitter](https://docs.rs/tauri/2.0.0/tauri/trait.Emitter.html)。

事件要么是全局的（投递给所有监听器），要么是 webview 特定的（只投递给与给定标签匹配的 webview）。

### 全局事件

要触发全局事件，你可以使用 [Emitter#emit](https://docs.rs/tauri/2.0.0/tauri/trait.Emitter.html#tymethod.emit) 函数：

```rust
use tauri::{AppHandle, Emitter};

#[tauri::command]
fn download(app: AppHandle, url: String) {
  app.emit("download-started", &url).unwrap();
  for progress in [1, 15, 50, 80, 100] {
    app.emit("download-progress", progress).unwrap();
  }
  app.emit("download-finished", &url).unwrap();
}
```

{{% alert title="注意" %}}
全局事件会投递给**所有**监听器
{{% /alert %}}

### Webview 事件

要触发事件给某个特定 webview 注册的监听器，你可以使用 [Emitter#emit_to](https://docs.rs/tauri/2.0.0/tauri/trait.Emitter.html#tymethod.emit_to) 函数：

```rust
use tauri::{AppHandle, Emitter};

#[tauri::command]
fn login(app: AppHandle, user: String, password: String) {
  let authenticated = user == "tauri-apps" && password == "tauri";
  let result = if authenticated { "loggedIn" } else { "invalidCredentials" };
  app.emit_to("login", "login-result", result).unwrap();
}
```

也可以通过调用 [Emitter#emit_filter](https://docs.rs/tauri/2.0.0/tauri/trait.Emitter.html#tymethod.emit_filter) 向一组 webview 触发事件。
在下面的示例中，我们向 main 和 file-viewer 两个 webview 发出 open-file 事件：

```rust
use tauri::{AppHandle, Emitter, EventTarget};

#[tauri::command]
fn open_file(app: AppHandle, path: std::path::PathBuf) {
  app.emit_filter("open-file", path, |target| match target {
    EventTarget::WebviewWindow { label } => label == "main" || label == "file-viewer",
    _ => false,
  }).unwrap();
}
```

{{% alert title="注意" %}}
Webview 特定的事件**不会**触发给普通的全局事件监听器。
要监听**任意**事件，你必须使用 `listen_any` 函数而不是 `listen`，它会让该监听器成为所有已发出事件的兜底监听器。
{{% /alert %}}

### 事件负载

事件负载可以是任何可[序列化](https://serde.rs/impl-serialize.html)且实现了 [Clone](https://doc.rust-lang.org/std/clone/trait.Clone.html) 的类型。
让我们用一个对象来增强 download 事件示例，在每个事件中传递更多信息：

```rust
use tauri::{AppHandle, Emitter};
use serde::Serialize;

#[derive(Clone, Serialize)]
#[serde(rename_all = "camelCase")]
struct DownloadStarted<'a> {
  url: &'a str,
  download_id: usize,
  content_length: usize,
}

#[derive(Clone, Serialize)]
#[serde(rename_all = "camelCase")]
struct DownloadProgress {
  download_id: usize,
  chunk_length: usize,
}

#[derive(Clone, Serialize)]
#[serde(rename_all = "camelCase")]
struct DownloadFinished {
  download_id: usize,
}

#[tauri::command]
fn download(app: AppHandle, url: String) {
  let content_length = 1000;
  let download_id = 1;

  app.emit("download-started", DownloadStarted {
    url: &url,
    download_id,
    content_length
  }).unwrap();

  for chunk_length in [15, 150, 35, 500, 300] {
    app.emit("download-progress", DownloadProgress {
      download_id,
      chunk_length,
    }).unwrap();
  }

  app.emit("download-finished", DownloadFinished { download_id }).unwrap();
}
```

### 监听事件

Tauri 提供了在 webview 与 Rust 两侧监听事件的 API。

#### 在前端监听事件

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

##### 常见陷阱

###### 不要在监听器兑现之前调用 `unlisten()`

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

###### setup 钩子中的时序问题

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

###### 事件顺序与异步监听器

事件监听器按注册顺序调用，但如果某个监听器是异步的，而事件发送方快速连续发送多个事件，监听器处理事件的顺序就可能错乱。对于需要保序的高吞吐数据投递，请考虑使用[通道](#通道)而不是事件系统。

##### 各框架的清理示例

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
更多信息请参阅[从前端调用 Rust](../3-callingrust/)文档。
{{% /alert %}}

##### 在 Rust 中监听事件

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

## 通道

事件系统被设计为应用中全局可用的简单双向通信。
在底层它会直接执行 JavaScript 代码，因此可能不适合发送大量数据。

通道（channel）被设计为快速且投递有序数据。它们在内部用于下载进度、子进程输出和 WebSocket 消息等流式操作。

让我们把 download 命令示例改写为使用通道而不是事件系统：

```rust
use tauri::{AppHandle, ipc::Channel};
use serde::Serialize;

#[derive(Clone, Serialize)]
#[serde(rename_all = "camelCase", rename_all_fields = "camelCase", tag = "event", content = "data")]
enum DownloadEvent<'a> {
  Started {
    url: &'a str,
    download_id: usize,
    content_length: usize,
  },
  Progress {
    download_id: usize,
    chunk_length: usize,
  },
  Finished {
    download_id: usize,
  },
}

#[tauri::command]
fn download(app: AppHandle, url: String, on_event: Channel<DownloadEvent>) {
  let content_length = 1000;
  let download_id = 1;

  on_event.send(DownloadEvent::Started {
    url: &url,
    download_id,
    content_length,
  }).unwrap();

  for chunk_length in [15, 150, 35, 500, 300] {
    on_event.send(DownloadEvent::Progress {
      download_id,
      chunk_length,
    }).unwrap();
  }

  on_event.send(DownloadEvent::Finished { download_id }).unwrap();
}
```

调用 download 命令时，你必须创建通道并把它作为参数传入：

```ts
import { invoke, Channel } from '@tauri-apps/api/core';

type DownloadEvent =
  | {
      event: 'started';
      data: {
        url: string;
        downloadId: number;
        contentLength: number;
      };
    }
  | {
      event: 'progress';
      data: {
        downloadId: number;
        chunkLength: number;
      };
    }
  | {
      event: 'finished';
      data: {
        downloadId: number;
      };
    };

const onEvent = new Channel<DownloadEvent>();
onEvent.onmessage = (message) => {
  console.log(`got download event ${message.event}`);
};

await invoke('download', {
  url: 'https://raw.githubusercontent.com/tauri-apps/tauri/dev/crates/tauri-schema-generator/schemas/config.schema.json',
  onEvent,
});
```

## 执行 JavaScript

要直接在 webview 上下文中执行任意 JavaScript 代码，你可以使用 [`WebviewWindow#eval`](https://docs.rs/tauri/2.0.0/tauri/webview/struct.WebviewWindow.html#method.eval) 函数：

```rust

tauri::Builder::default()
  .setup(|app| {
    let webview = app.get_webview_window("main").unwrap();
    webview.eval("console.log('hello from Rust')")?;
    Ok(())
  })
```

如果要执行的脚本比较复杂，必须使用 Rust 对象的输入，我们推荐使用 [serialize-to-javascript](https://docs.rs/serialize-to-javascript/latest/serialize_to_javascript/) crate。
