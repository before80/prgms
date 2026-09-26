+++
title = "26 Store"
date = 2026-09-25T21:31:08+08:00
weight = 26
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/plugin/store/](https://tauri.app/plugin/store/)

提供持久化的键值存储，可把状态保存到文件并按需加载。

## 支持的平台

| 平台 | 支持程度 | 说明 |
| --- | --- | --- |
| Windows | 完整支持 |  |
| Linux | 完整支持 |  |
| macOS | 完整支持 |  |
| Android | 完整支持 |  |
| iOS | 完整支持 |  |

## 设置

### 自动

使用你的项目包管理器添加依赖：

{{< tabpane text=true persist=disabled >}}

{{% tab header="npm" %}}

```sh
npm run tauri add store
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn run tauri add store
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm tauri add store
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno task tauri add store
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun tauri add store
```

{{% /tab %}}

{{% tab header="cargo" %}}

```sh
cargo tauri add store
```

{{% /tab %}}

{{< /tabpane >}}

### 手动

1. 在 `src-tauri` 文件夹中运行以下命令，把插件加入 `Cargo.toml` 里的项目依赖：

   ```sh
   cargo add tauri-plugin-store
   ```

2. 修改 `lib.rs` 初始化插件：

   ```rust
   #[cfg_attr(mobile, tauri::mobile_entry_point)]
   pub fn run() {
       tauri::Builder::default()
           .plugin(tauri_plugin_store::init())
           .run(tauri::generate_context!())
           .expect("error while running tauri application");
   }
   ```

3. 用你偏好的 JavaScript 包管理器安装 JavaScript 端绑定：

{{< tabpane text=true persist=disabled >}}

{{% tab header="npm" %}}

```sh
npm install @tauri-apps/plugin-store
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn add @tauri-apps/plugin-store
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm add @tauri-apps/plugin-store
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno add npm:@tauri-apps/plugin-store
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun add @tauri-apps/plugin-store
```

{{% /tab %}}

{{< /tabpane >}}


## 用法

**语言**

{{< tabpane text=true persist=disabled >}}

{{% tab header="JavaScript" %}}

```typescript
import { load } from '@tauri-apps/plugin-store';
// 使用 `"withGlobalTauri": true` 时，你可以这样写
// const { load } = window.__TAURI__.store;

// 创建一个新 store 或加载已有 store；
// 注意如果该路径的 `Store` 已经创建过，这些选项会被忽略
const store = await load('store.json', { autoSave: false });

// 设置一个值。
await store.set('some-key', { value: 5 });

// 读取一个值。
const val = await store.get<{ value: number }>('some-key');
console.log(val); // { value: 5 }

// 你可以在修改后手动保存 store。
// 否则它会在正常退出时保存。
// 如果你把 `autoSave` 设为某个数字或留空，
// 它会在防抖延迟后把改动写入磁盘，默认 100ms。
await store.save();
```

{{% /tab %}}

{{% tab header="Rust" %}}

```rust
use tauri::Wry;
use tauri_plugin_store::StoreExt;
use serde_json::json;

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_store::Builder::default().build())
        .setup(|app| {
            // 创建一个新 store 或加载已有 store；
            // 这还会把该 store 放进应用的资源表，
            // 因此你后续的 `store` 调用（无论来自 Rust 还是 JS）
            // 都会复用同一个 store。

            let store = app.store("store.json")?;

            // 注意值必须是 serde_json::Value 实例，
            // 否则它们与 JavaScript 绑定不兼容。
            store.set("some-key", json!({ "value": 5 }));

            // 从 store 中读取一个值。
            let value = store.get("some-key").expect("Failed to get value from store");
            println!("{}", value); // {"value":5}

            // 把该 store 从资源表中移除
            store.close_resource();

            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

{{% /tab %}}

{{< /tabpane >}}

### LazyStore

还有一个更高级的 JavaScript API `LazyStore`，它只在首次访问时加载 store：

```typescript
import { LazyStore } from '@tauri-apps/plugin-store';

const store = new LazyStore('settings.json');
```

## 从 v1 以及 v2 beta/rc 迁移

**语言**

{{< tabpane text=true persist=disabled >}}

{{% tab header="JavaScript" %}}

```diff
- import { Store } from '@tauri-apps/plugin-store';
+ import { LazyStore } from '@tauri-apps/plugin-store';
```

{{% /tab %}}

{{% tab header="Rust" %}}

```diff
- with_store(app.handle().clone(), stores, path, |store| {
-     store.insert("some-key".to_string(), json!({ "value": 5 }))?;
-     Ok(())
- });
+ let store = app.store(path)?;
+ store.set("some-key".to_string(), json!({ "value": 5 }));
```

{{% /tab %}}

{{< /tabpane >}}

## 权限

默认情况下，所有有潜在危险的插件命令和作用域都被阻止，无法访问。你必须在 `capabilities` 配置中修改权限才能启用它们。

更多信息请参阅[能力概述](../../security/4-capabilities/)，以及[使用插件权限的分步指南](../../learn/security/1-usingpluginpermissions/)。

```json
{
  "permissions": [
    ...,
    "store:default"
  ]
}
```
