+++
title = "14 Localhost"
date = 2026-09-25T21:31:08+08:00
weight = 14
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/plugin/localhost/](https://tauri.app/plugin/localhost/)

通过 localhost 服务器暴露应用的资源，而不是使用默认的自定义协议。

{{% alert title="警告" color="warning" %}}
这个插件会带来相当大的安全风险，只有在你清楚自己在做什么时才应使用它。如果有疑问，请使用默认的自定义协议实现。
{{% /alert %}}

## 支持的平台

| 平台 | 支持程度 | 说明 |
| --- | --- | --- |
| Windows | 完整支持 |  |
| Linux | 完整支持 |  |
| macOS | 完整支持 |  |
| Android | 不支持 |  |
| iOS | 不支持 |  |

## 设置

安装 localhost 插件即可开始。

**安装方式**

### 自动

使用你的项目包管理器添加依赖：

{{< tabpane text=true persist=disabled >}}
{{% tab header="npm" %}}

```sh
npm run tauri add localhost
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn run tauri add localhost
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm tauri add localhost
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno task tauri add localhost
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun tauri add localhost
```

{{% /tab %}}

{{% tab header="cargo" %}}

```sh
cargo tauri add localhost
```

{{% /tab %}}

{{< /tabpane >}}

### 手动

1. 在 `src-tauri` 文件夹中运行以下命令，把插件加入 `Cargo.toml` 里的项目依赖：

   ```sh
   cargo add tauri-plugin-localhost
   ```

2. 修改 `lib.rs` 初始化插件：

   ```rust
   #[cfg_attr(mobile, tauri::mobile_entry_point)]
   pub fn run() {
       tauri::Builder::default()
           .plugin(tauri_plugin_localhost::Builder::new().build())
           .run(tauri::generate_context!())
           .expect("error while running tauri application");
   }
   ```

## 用法

localhost 插件在 Rust 中可用。

```rust
use tauri::{webview::WebviewWindowBuilder, WebviewUrl};

pub fn run() {
  let port: u16 = 9527;

  tauri::Builder::default()
      .plugin(tauri_plugin_localhost::Builder::new(port).build())
      .setup(move |app| {
          let url = format!("http://localhost:{}", port).parse().unwrap();
          WebviewWindowBuilder::new(app, "main".to_string(), WebviewUrl::External(url))
              .title("Localhost Example")
              .build()?;
          Ok(())
      })
      .run(tauri::generate_context!())
      .expect("error while running tauri application");
}
```
