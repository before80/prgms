+++
title = "13 HTTP Client"
date = 2026-09-25T21:31:08+08:00
weight = 13
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/plugin/http-client/](https://tauri.app/plugin/http-client/)

使用 http 插件发起 HTTP 请求。

## 支持的平台

| 平台 | 支持程度 | 说明 |
| --- | --- | --- |
| Windows | 完整支持 |  |
| Linux | 完整支持 |  |
| macOS | 完整支持 |  |
| Android | 完整支持 |  |
| iOS | 完整支持 |  |

## 设置

{{< tabpane text=true persist=disabled >}}

{{% tab header="自动" %}}

使用你的项目包管理器添加依赖：

{{< tabpane text=true persist=disabled >}}

{{% tab header="npm" %}}

```sh
npm run tauri add http
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn run tauri add http
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm tauri add http
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno task tauri add http
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun tauri add http
```

{{% /tab %}}

{{% tab header="cargo" %}}

```sh
cargo tauri add http
```

{{% /tab %}}

{{< /tabpane >}}

{{% /tab %}}

{{% tab header="手动" %}}

1. 在 `src-tauri` 文件夹中运行以下命令，把插件加入 `Cargo.toml` 里的项目依赖：

   ```sh
   cargo add tauri-plugin-http
   ```

2. 修改 `lib.rs` 初始化插件：

   ```rust
   #[cfg_attr(mobile, tauri::mobile_entry_point)]
   pub fn run() {
       tauri::Builder::default()
           .plugin(tauri_plugin_http::init())
           .run(tauri::generate_context!())
           .expect("error while running tauri application");
   }
   ```

3. 用你偏好的 JavaScript 包管理器安装 JavaScript 端绑定：

{{< tabpane text=true persist=disabled >}}

{{% tab header="npm" %}}

```sh
npm install @tauri-apps/plugin-http
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn add @tauri-apps/plugin-http
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm add @tauri-apps/plugin-http
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno add npm:@tauri-apps/plugin-http
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun add @tauri-apps/plugin-http
```

{{% /tab %}}

{{< /tabpane >}}

{{% /tab %}}

{{< /tabpane >}}

## 用法

HTTP 插件在 Rust 中作为 [reqwest](https://docs.rs/reqwest/) 的重新导出可用，在 JavaScript 中也可用。

### JavaScript

1. 配置允许的 URL

   ```json
   //src-tauri/capabilities/default.json
   {
     "permissions": [
       {
         "identifier": "http:default",
         "allow": [{ "url": "https://*.tauri.app" }],
         "deny": [{ "url": "https://private.tauri.app" }]
       }
     ]
   }
   ```

   更多信息请参阅[权限概述](../../security/2-permissions/)文档。

2. 发送请求

   `fetch` 方法尽可能贴近并符合 [`fetch` Web API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)。

   ```javascript
   import { fetch } from '@tauri-apps/plugin-http';

   // 发送 GET 请求
   const response = await fetch('http://test.tauri.app/data.json', {
     method: 'GET',
   });
   console.log(response.status); // 例如 200
   console.log(response.statusText); // 例如 "OK"
   ```

   {{% alert title="注意" %}}

   [被禁止的请求头](https://fetch.spec.whatwg.org/#terminology-headers)默认会被忽略。要使用它们，你必须启用 `unsafe-headers` 特性标志：

   ```toml
   [dependencies]
   tauri-plugin-http = { version = "2", features = ["unsafe-headers"] }
   ```

   {{% /alert %}}

### Rust

在 Rust 中你可以使用该插件重新导出的 `reqwest` crate。更多细节请参阅 [reqwest 文档](https://docs.rs/reqwest/)。

```rust

let res = reqwest::get("http://my.api.host/data.json").await;
println!("{:?}", res.status()); // 例如 200
println!("{:?}", res.text().await); // 例如 Ok("{ Content }")
```

## 权限

默认情况下，所有有潜在危险的插件命令和作用域都被阻止，无法访问。你必须在 `capabilities` 配置中修改权限才能启用它们。

更多信息请参阅[能力概述](../../security/4-capabilities/)，以及[使用插件权限的分步指南](../../learn/security/1-usingpluginpermissions/)。

```json
{
  "permissions": [
    ...,
    "http:default"
  ]
}
```
