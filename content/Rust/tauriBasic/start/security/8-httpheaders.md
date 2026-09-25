+++
title = "7 HTTP 头"
date = 2026-09-25T21:31:08+08:00
weight = 7
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/security/http-headers/](https://tauri.app/security/http-headers/)

*需要 Tauri 2.1.0 或更高版本。*

在配置中定义的头会随响应一起发送给 webview。
这不包括 IPC 消息和错误响应。
更具体地说，通过 [crates/tauri/src/protocol/tauri.rs ↗](https://github.com/tauri-apps/tauri/blob/8e8312bb8201ccc609e4bbc1a990bdc314daa00f/crates/tauri/src/protocol/tauri.rs#L103) 中的 `get_response` 函数发送的每个响应都会包含这些头。

### 头名称

头名称仅限于：

- [Access-Control-Allow-Credentials ↗](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Access-Control-Allow-Credentials)
- [Access-Control-Allow-Headers ↗](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Access-Control-Allow-Headers)
- [Access-Control-Allow-Methods ↗](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Access-Control-Allow-Methods)
- [Access-Control-Expose-Headers ↗](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Access-Control-Expose-Headers)
- [Access-Control-Max-Age ↗](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Access-Control-Max-Age)
- [Cross-Origin-Embedder-Policy ↗](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cross-Origin-Embedder-Policy)
- [Cross-Origin-Opener-Policy ↗](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cross-Origin-Opener-Policy)
- [Cross-Origin-Resource-Policy ↗](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cross-Origin-Resource-Policy)
- [Permissions-Policy ↗](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Permissions-Policy)
- [Service-Worker-Allowed ↗](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Service-Worker-Allowed)
- [Timing-Allow-Origin ↗](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Timing-Allow-Origin)
- [X-Content-Type-Options ↗](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Content-Type-Options)
- Tauri-Custom-Header

{{% alert title="注意" %}}
`Tauri-Custom-Header` 不适用于生产环境。
{{% /alert %}}

{{% alert title="注意" %}}
[内容安全策略（CSP）](../6-csp/)不在这里定义。
{{% /alert %}}

### 如何配置头

- 用一个字符串
- 用字符串数组
- 用对象／键值对，其中值必须是字符串
- 用 null

头的值在实际响应中总会被转换为字符串。根据配置文件的写法，有些头的值需要组合。组合的规则如下：

- `string`：作为结果的头值保持不变
- `array`：各项用 `, ` 连接，作为结果的头值
- `key-value`：各项由 键 + 空格 + 值 组成，各项之间再用 `; ` 连接，作为结果的头值
- `null`：该头会被忽略

### 示例

```javascript
{
 //...
  "app":{
    //...
    "security": {
      //...
      "headers": {
        "Cross-Origin-Opener-Policy": "same-origin",
        "Cross-Origin-Embedder-Policy": "require-corp",
        "Timing-Allow-Origin": [
          "https://developer.mozilla.org",
          "https://example.com",
        ],
        "X-Content-Type-Options": null, // 会被忽略
        "Access-Control-Expose-Headers": "Tauri-Custom-Header",
        "Tauri-Custom-Header": {
          "key1": "'value1' 'value2'",
          "key2": "'value3'"
        }
      },
      // 注意 CSP 不是在 headers 下定义的
      "csp": "default-src 'self'; connect-src ipc: http://ipc.localhost",
    }
  }
}
```

{{% alert title="注意" %}}
`Tauri-Custom-Header` 不适用于生产环境。
用于测试时：记得相应设置 `Access-Control-Expose-Headers`。
{{% /alert %}}

在这个示例中，`Cross-Origin-Opener-Policy` 和 `Cross-Origin-Embedder-Policy` 的设置是为了允许使用 [`SharedArrayBuffer` ↗](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/SharedArrayBuffer)。
`Timing-Allow-Origin` 允许从所列网站加载的脚本通过 [Resource Timing API ↗](https://developer.mozilla.org/en-US/docs/Web/API/Performance_API/Resource_timing) 访问详细的网络计时数据。

对 helloworld 示例来说，该配置会产生：

```http
access-control-expose-headers: Tauri-Custom-Header
content-security-policy: default-src 'self'; connect-src ipc: http://ipc.localhost; script-src 'self' 'sha256-Wjjrs6qinmnr+tOry8x8PPwI77eGpUFR3EEGZktjJNs='
content-type: text/html
cross-origin-embedder-policy: require-corp
cross-origin-opener-policy: same-origin
tauri-custom-header: key1 'value1' 'value2'; key2 'value3'
timing-allow-origin: https://developer.mozilla.org, https://example.com
```

### 框架

有些开发环境需要额外设置，才能模拟生产环境。

{{% alert title="注意" %}}
要让这些框架下的头生效，你可能需要同时在框架配置（用于开发模式）和 Tauri 配置（用于构建模式）中定义它们。原因如下：
- 框架在构建时不会包含其配置文件中定义的头。
- Tauri 无法向框架的开发服务器注入头，它只能向最终构建产物注入头。
{{% /alert %}}

#### JavaScript/TypeScript

对于使用构建工具 **Vite** 的项目（包括 **Qwik、React、Solid、Svelte 和 Vue**），把想要的头加入 `vite.config.ts`。

```typescript
import { defineConfig } from 'vite';

export default defineConfig({
  // ...
  server: {
      // ...
      headers: {
        'Cross-Origin-Opener-Policy': 'same-origin',
        'Cross-Origin-Embedder-Policy': 'require-corp',
        'Timing-Allow-Origin': 'https://developer.mozilla.org, https://example.com',
        'Access-Control-Expose-Headers': 'Tauri-Custom-Header',
        'Tauri-Custom-Header': "key1 'value1' 'value2'; key2 'value3'"
      },
    },
})
```

有时 `vite.config.ts` 会集成到框架的配置文件中，但设置方式不变。
如果是 **Angular**，请把它们加入 `angular.json`。

```json
{
  //...
  "projects":{
    //...
    "insert-project-name":{
      //...
      "architect":{
        //...
        "serve":{
          //...
          "options":{
            //...
            "headers":{
              "Cross-Origin-Opener-Policy": "same-origin",
              "Cross-Origin-Embedder-Policy": "require-corp",
              "Timing-Allow-Origin": "https://developer.mozilla.org, https://example.com",
              "Access-Control-Expose-Headers": "Tauri-Custom-Header",
              "Tauri-Custom-Header": "key1 'value1' 'value2'; key2 'value3'"
            }
          }
        }
      }
    }
  }
}
```

如果是 **Nuxt**，请把它们加入 `nuxt.config.ts`。

```typescript
export default defineNuxtConfig({
  //...
  vite: {
    //...
    server: {
      //...
      headers:{
        'Cross-Origin-Opener-Policy': 'same-origin',
        'Cross-Origin-Embedder-Policy': 'require-corp',
        'Timing-Allow-Origin': 'https://developer.mozilla.org, https://example.com',
        'Access-Control-Expose-Headers': 'Tauri-Custom-Header',
        'Tauri-Custom-Header': "key1 'value1' 'value2'; key2 'value3'"
      }
    },
  },
});
```

**Next.js** 不依赖 **Vite**，所以做法不同。
更多信息请[见这里 ↗](https://nextjs.org/docs/pages/api-reference/next-config-js/headers)。
这些头在 `next.config.js` 中定义。

```javascript
module.exports = {
  //...
  async headers() {
    return [
      {
        source: '/*',
        headers: [
          {
            key: 'Cross-Origin-Opener-Policy',
            value: 'same-origin',
          },
          {
            key: 'Cross-Origin-Embedder-Policy',
            value: 'require-corp',
          },
          {
            key: 'Timing-Allow-Origin',
            value: 'https://developer.mozilla.org, https://example.com',
          },
          {
            key: 'Access-Control-Expose-Headers',
            value: 'Tauri-Custom-Header',
          },
          {
            key: 'Tauri-Custom-Header',
            value: "key1 'value1' 'value2'; key2 'value3'",
          },
        ],
      },
    ]
  },
}
```

#### Rust

对于 **Yew** 和 **Leptos**，请把这些头加入 `Trunk.toml`。

```toml
[serve]
#...
headers = { 
  "Cross-Origin-Opener-Policy" = "same-origin",
  "Cross-Origin-Embedder-Policy" = "require-corp",
  "Timing-Allow-Origin" = "https://developer.mozilla.org, https://example.com",
  "Access-Control-Expose-Headers" = "Tauri-Custom-Header",
  "Tauri-Custom-Header" = "key1 'value1' 'value2'; key2 'value3'"
}

```
