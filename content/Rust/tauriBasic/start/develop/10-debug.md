+++
title = "1 调试概述"
date = 2026-09-25T21:31:08+08:00
weight = 10
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/develop/debug/](https://tauri.app/develop/debug/)

Tauri 涉及的环节很多，你可能会遇到需要调试的问题。有许多地方会打印错误细节，Tauri 也提供了一些工具来让调试过程更直接。

## 仅在开发环境使用的代码

调试工具箱中最有用的工具之一，是能在代码里添加调试语句。不过你通常不希望它们进入生产环境，这时判断自己是否运行在开发模式下就派上用场了。

### 在 Rust 中

```rust
fn main() {
  // 当前实例是否由 `tauri dev` 启动。
  #[cfg(dev)]
  {
    // 仅 `tauri dev` 的代码
  }
  if cfg!(dev) {
    // 仅 `tauri dev` 的代码
  } else {
    // 仅 `tauri build` 的代码
  }
  let is_dev: bool = tauri::is_dev();

  // 是否启用了调试断言。对 `tauri dev` 和 `tauri build --debug` 都为 true。
  #[cfg(debug_assertions)]
  {
    // 仅调试的代码
  }
  if cfg!(debug_assertions) {
    // 仅调试的代码
  } else {
    // 仅生产环境的代码
  }
}
```

## Rust 控制台

首先要找错误的地方是 Rust 控制台，也就是你运行 `tauri dev` 等命令的终端。你可以在 Rust 文件中用以下代码向该控制台打印内容：

```rust
println!("Message from Rust: {}", msg);
```

有时你的 Rust 代码可能出错，Rust 编译器会提供大量信息。例如，如果 `tauri dev` 崩溃，你可以在 Linux 和 macOS 上这样重新运行：

```shell
RUST_BACKTRACE=1 tauri dev
```

在 Windows（PowerShell）上这样运行：

```powershell
tauri dev
```

该命令会给出细粒度的堆栈跟踪。一般来说，Rust 编译器会通过提供问题的详细信息来帮助你，例如：

```bash
  --> src/main.rs:11:5
   |
11 |     sun += i.to_string().parse::<u64>().unwrap();
   |     ^^^ help: a local variable with a similar name exists: `sum`

error: aborting due to previous error

For more information about this error, try `rustc --explain E0425`.
```

## WebView 控制台

在 WebView 中右键，选择 `Inspect Element`。这会打开一个与你熟悉的 Chrome 或 Firefox 开发者工具类似的 Web 检查器。
你也可以使用 Linux 和 Windows 上的 `Ctrl + Shift + i` 快捷键，以及 macOS 上的 `Command + Option + i` 打开检查器。

检查器是平台特定的：在 Linux 上渲染 webkit2gtk WebInspector，在 macOS 上使用 Safari 的检查器，在 Windows 上使用 Microsoft Edge DevTools。

### 以编程方式打开 Devtools

你可以通过 [`WebviewWindow::open_devtools`](https://docs.rs/tauri/2.0.0/tauri/webview/struct.WebviewWindow.html#method.open_devtools) 和 [`WebviewWindow::close_devtools`](https://docs.rs/tauri/2.0.0/tauri/webview/struct.WebviewWindow.html#method.close_devtools) 函数控制检查器窗口的可见性：

```rust
  .setup(|app| {
    #[cfg(debug_assertions)] // 仅在调试构建中包含这段代码
    {
      let window = app.get_webview_window("main").unwrap();
      window.open_devtools();
      window.close_devtools();
    }
    Ok(())
  });
```

### 在生产环境中使用检查器

默认情况下，检查器只在开发和调试构建中启用，除非你通过 Cargo 特性启用它。

#### 创建调试构建

要创建调试构建，请运行 `tauri build --debug` 命令。

{{< tabpane text=true persist=disabled >}}
{{% tab header="npm" %}}

```sh
npm run tauri build -- --debug
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn tauri build --debug
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm tauri build --debug
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno task tauri build --debug
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun tauri build --debug
```

{{% /tab %}}

{{% tab header="cargo" %}}

```sh
cargo tauri build --debug
```

{{% /tab %}}

{{< /tabpane >}}
与普通的构建和开发流程一样，第一次运行该命令需要一些时间，但后续运行会快得多。
最终打包出的应用启用了开发控制台，位于 `src-tauri/target/debug/bundle`。

你也可以从终端运行已构建的应用，从而获得 Rust 编译器的提示（出错时）或你的 `println` 消息。进入文件 `src-tauri/target/(release|debug)/[app name]`，直接在控制台中运行它，或在文件系统中双击该可执行文件（注意：用这种方式时出错会导致控制台关闭）。

##### 启用 Devtools 特性

{{% alert title="危险" color="warning" %}}

devtools API 在 macOS 上是私有的。在 macOS 上使用私有 API 会导致你的应用无法被 App Store 接受。

{{% /alert %}}

要在**生产构建**中启用 devtools，你必须在 `src-tauri/Cargo.toml` 文件中启用 `devtools` Cargo 特性：

```toml
tauri = { version = "...", features = ["...", "devtools"] }
```

## 调试核心进程

核心进程由 Rust 驱动，因此你可以使用 GDB 或 LLDB 调试它。你可以按照 [VS Code 中的调试](../15-vscode/)指南，了解如何使用 LLDB VS Code 扩展来调试 Tauri 应用的核心进程。
