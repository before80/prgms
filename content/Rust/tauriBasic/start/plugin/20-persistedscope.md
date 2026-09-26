+++
title = "20 Persisted Scope"
date = 2026-09-25T21:31:08+08:00
weight = 20
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/plugin/persisted-scope/](https://tauri.app/plugin/persisted-scope/)

保存文件系统与资源作用域，并在应用重新打开时恢复它们。

## 支持的平台

| 平台 | 支持程度 | 说明 |
| --- | --- | --- |
| Windows | 完整支持 |  |
| Linux | 完整支持 |  |
| macOS | 完整支持 |  |
| Android | 完整支持 |  |
| iOS | 完整支持 |  |

## 设置

安装 persisted-scope 插件即可开始。

**安装方式**

### 自动

使用你的项目包管理器添加依赖：

{{< tabpane text=true persist=disabled >}}
{{% tab header="npm" %}}

```sh
npm run tauri add persisted-scope
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn run tauri add persisted-scope
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm tauri add persisted-scope
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno task tauri add persisted-scope
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun tauri add persisted-scope
```

{{% /tab %}}

{{% tab header="cargo" %}}

```sh
cargo tauri add persisted-scope
```

{{% /tab %}}

{{< /tabpane >}}

### 手动

1. 在 `src-tauri` 文件夹中运行以下命令，把插件加入 `Cargo.toml` 里的项目依赖：

   ```sh
   cargo add tauri-plugin-persisted-scope
   ```

2. 修改 `lib.rs` 初始化插件：

   ```rust
   #[cfg_attr(mobile, tauri::mobile_entry_point)]
   pub fn run() {
       tauri::Builder::default()
           .plugin(tauri_plugin_persisted_scope::init())
           .run(tauri::generate_context!())
           .expect("error while running tauri application");
   }
   ```

{{% alert title="警告" color="warning" %}}
`persisted-scope` 插件**必须**在 `fs` 插件之后注册和初始化，如下例所示：

```rust
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_fs::init()) // fs 必须在 persisted scope 之前！
        .plugin(tauri_plugin_persisted_scope::init())
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

**否则持久化作用域将无法工作！** 在开发模式下启动应用时，你还应该会看到类似这样的警告信息：

```
Please make sure to register the `fs` plugin before the `persisted-scope` plugin!
```

{{% /alert %}}

## 用法

设置完成后，该插件会自动保存并恢复文件系统与资源作用域。
