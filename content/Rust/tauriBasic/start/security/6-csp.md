+++
title = "6 内容安全策略（CSP）"
date = 2026-09-25T21:31:08+08:00
weight = 6
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/security/csp/](https://tauri.app/security/csp/)

Tauri 会限制你 HTML 页面的[内容安全策略](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP)（CSP）。
这可以用来减少或防止跨站脚本（XSS）等常见 Web 漏洞的影响。

本地脚本会做哈希处理，样式和外部脚本则使用密码学 nonce 引用，从而阻止未允许的内容被加载。

{{% alert title="警告" color="warning" %}}
避免加载 CDN 提供的脚本之类的远程内容，因为它们会引入攻击面。一般来说，任何不受信任的文件都可能引入新的、不易察觉的攻击面。
{{% /alert %}}

只有在 Tauri 配置文件中设置了 CSP，CSP 防护才会启用。
你应当尽可能严格地限制它，只允许 webview 从你信任（最好是你自己拥有）的主机加载资源。
在编译期，Tauri 会自动把自己的 nonce 和哈希追加到打包代码与资源相关的 CSP 属性上，因此你只需关注自己应用特有的部分。

下面这个 CSP 配置示例取自 Tauri 的 [`api`](https://github.com/tauri-apps/tauri/blob/dev/examples/api/src-tauri/tauri.conf.json#L22) 示例，但每个应用开发者都需要根据自己的应用需求做调整。

```json
  "csp": {
        "default-src": "'self' customprotocol: asset:",
        "connect-src": "ipc: http://ipc.localhost",
        "font-src": ["https://fonts.gstatic.com"],
        "img-src": "'self' asset: http://asset.localhost blob: data:",
        "style-src": "'unsafe-inline' 'self' https://fonts.googleapis.com"
      },
```

{{% alert title="提示" %}}
当你用 Rust 开发前端，或者前端以其它方式使用 WebAssembly 时，记得把 `'wasm-unsafe-eval'` 加入 `script-src`。
{{% /alert %}}

关于这项防护的更多信息，请参阅 [`script-src`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/script-src)、[`style-src`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/style-src) 和 [CSP 来源](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/Sources#sources)。
