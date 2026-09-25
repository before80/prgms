+++
title = "5 状态管理"
date = 2026-09-25T21:31:08+08:00
weight = 5
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/develop/state-management/](https://tauri.app/develop/state-management/)

在 Tauri 应用中，你经常需要跟踪应用的当前状态，或者管理与应用相关联事物的生命周期。Tauri 通过 [`Manager`](https://docs.rs/tauri/latest/tauri/trait.Manager.html) API 提供了一种简单的方式来管理应用状态，并在命令被调用时读取它。

下面是一个简单示例：

```rust
use tauri::{Builder, Manager};

struct AppData {
  welcome_message: &'static str,
}

fn main() {
  Builder::default()
    .setup(|app| {
      app.manage(AppData {
        welcome_message: "Welcome to Tauri!",
      });
      Ok(())
    })
    .run(tauri::generate_context!())
    .unwrap();
}
```

之后你可以用任何实现了 [`Manager`](https://docs.rs/tauri/latest/tauri/trait.Manager.html) trait 的类型访问状态，例如 [`App`](https://docs.rs/tauri/latest/tauri/struct.App.html) 实例：

```rust
let data = app.state::<AppData>();
```

更多信息（包括在命令中访问状态）请参阅[访问状态](#访问状态)一节。

## 可变性

在 Rust 中，你不能直接修改在多个线程之间共享的值，或者通过 [`Arc`](https://doc.rust-lang.org/stable/std/sync/struct.Arc.html)（或 Tauri 的 [`State`](https://docs.rs/tauri/latest/tauri/struct.State.html)）这类共享指针控制所有权的值。这样做可能导致数据竞争（例如两次写入同时发生）。

要绕过这一点，你可以使用一种称为[内部可变性](https://doc.rust-lang.org/book/ch15-05-interior-mutability.html)的概念。例如，可以用标准库的 [`Mutex`](https://doc.rust-lang.org/stable/std/sync/struct.Mutex.html) 包裹你的状态。这样你就可以在需要修改时锁定该值，完成后解锁。

```rust

use tauri::{Builder, Manager};

#[derive(Default)]
struct AppState {
  counter: u32,
}

fn main() {
  Builder::default()
    .setup(|app| {
      app.manage(Mutex::new(AppState::default()));
      Ok(())
    })
    .run(tauri::generate_context!())
    .unwrap();
}
```

现在可以通过锁定互斥锁来修改状态：

```rust

// 锁定互斥锁以获得可变访问：
let mut state = state.lock().unwrap();

// 修改状态：
state.counter += 1;
```

在作用域结束时，或者 `MutexGuard` 被以其它方式丢弃时，互斥锁会自动解锁，以便应用中的其它部分访问并修改其中的数据。

### 何时使用异步互斥锁

引用 [Tokio 文档](https://docs.rs/tokio/latest/tokio/sync/struct.Mutex.html#which-kind-of-mutex-should-you-use)的说法，通常使用标准库的 [`Mutex`](https://doc.rust-lang.org/stable/std/sync/struct.Mutex.html) 而不是 Tokio 提供的异步互斥锁是没问题的：

> 与流行的看法相反，在异步代码中使用标准库的普通 Mutex 是可以的，而且往往更受推荐……异步互斥锁的主要用例是为数据库连接这类 IO 资源提供共享可变访问。

完整阅读链接的文档以理解两者之间的取舍是个好主意。你_确实_需要异步互斥锁的一种情形是：你需要在 await 点之间持有 `MutexGuard`。

### 你需要 `Arc` 吗？

在 Rust 中经常看到用 [`Arc`](https://doc.rust-lang.org/stable/std/sync/struct.Arc.html) 在多个线程间共享值的所有权（通常与 [`Mutex`](https://doc.rust-lang.org/stable/std/sync/struct.Mutex.html) 搭配成 `Arc<Mutex<T>>`）。不过，对于存放在 [`State`](https://docs.rs/tauri/latest/tauri/struct.State.html) 中的东西，你不需要使用 [`Arc`](https://doc.rust-lang.org/stable/std/sync/struct.Arc.html)，因为 Tauri 会替你处理。

如果 `State` 的生命周期要求使你无法把状态移动到新线程中，你可以改为把 `AppHandle` 移动到该线程，然后按下文“[使用 Manager trait 访问状态](#使用-manager-trait-访问状态)”一节所示取出状态。`AppHandle` 的克隆开销被刻意设计得很低，正适合这种用例。

## 访问状态

### 在命令中访问状态

```rust
fn increase_counter(state: State<'_, Mutex<AppState>>) -> u32 {
  let mut state = state.lock().unwrap();
  state.counter += 1;
  state.counter
}
```

关于命令的更多信息，请参阅[从前端调用 Rust](../3-callingrust/)。

#### 异步命令

如果你使用 `async` 命令并想使用 Tokio 的异步 [`Mutex`](https://docs.rs/tokio/latest/tokio/sync/struct.Mutex.html)，可以用同样的方式设置，并这样访问状态：

```rust
async fn increase_counter(state: State<'_, Mutex<AppState>>) -> Result<u32, ()> {
  let mut state = state.lock().await;
  state.counter += 1;
  Ok(state.counter)
}
```

注意如果你使用异步命令，返回类型必须是 [`Result`](https://doc.rust-lang.org/stable/std/result/index.html)。

### 使用 [`Manager`](https://docs.rs/tauri/latest/tauri/trait.Manager.html) trait 访问状态

有时你可能需要在命令之外访问状态，例如在另一个线程中，或在 `on_window_event` 这类事件处理函数中。这种情况下，你可以使用实现了 [`Manager`](https://docs.rs/tauri/latest/tauri/trait.Manager.html) trait 的类型（例如 `AppHandle`）的 `state()` 方法获取状态：

```rust
use tauri::{Builder, Window, WindowEvent, Manager};

#[derive(Default)]
struct AppState {
  counter: u32,
}

// 在事件处理函数中：
fn on_window_event(window: &Window, _event: &WindowEvent) {
    // 获取 app 的句柄，以便取得全局状态。
    let app_handle = window.app_handle();
    let state = app_handle.state::<Mutex<AppState>>();

    // 锁定互斥锁以可变地访问状态。
    let mut state = state.lock().unwrap();
    state.counter += 1;
}

fn main() {
  Builder::default()
    .setup(|app| {
      app.manage(Mutex::new(AppState::default()));
      Ok(())
    })
    .on_window_event(on_window_event)
    .run(tauri::generate_context!())
    .unwrap();
}
```

当你无法依赖命令注入时，这个方法很有用。例如，当你需要把状态移动到使用 `AppHandle` 更方便的线程中，或者你不在命令上下文中时。

## 类型不匹配

{{% alert title="警告" color="warning" %}}
如果你为 [`State`](https://docs.rs/tauri/latest/tauri/struct.State.html) 参数使用了错误的类型，运行时会发生 panic，而不是编译期报错。

例如，如果你使用 `State<'_, AppState>` 而不是 `State<'_, Mutex<AppState>>`，就不会有任何以该类型托管的状态。
{{% /alert %}}

如果你愿意，可以用类型别名包裹状态以避免这个错误：

```rust

#[derive(Default)]
struct AppStateInner {
  counter: u32,
}

type AppState = Mutex<AppStateInner>;
```

不过，请确保按原样使用类型别名，不要再把它包一层 [`Mutex`](https://doc.rust-lang.org/stable/std/sync/struct.Mutex.html)，否则你会遇到同样的问题。
