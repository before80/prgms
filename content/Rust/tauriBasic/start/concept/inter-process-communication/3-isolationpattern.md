+++
title = "3 Isolation 模式"
date = 2026-09-25T21:31:08+08:00
weight = 3
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/concept/inter-process-communication/isolation/](https://tauri.app/concept/inter-process-communication/isolation/)

Isolation 模式是一种用 JavaScript 拦截并修改前端发出的 Tauri API 消息、使其在到达 Tauri 核心之前被处理的方式。由 Isolation 模式注入的安全 JavaScript 代码被称为 Isolation 应用。

## 为什么需要它

Isolation 模式的目的是为开发者提供一种机制，帮助保护应用免受前端对 Tauri 核心的不必要或恶意调用。Isolation 模式的需求源自运行在前端的不受信任内容所带来的威胁，这对依赖众多的应用来说是常见情况。关于应用可能面临的众多威胁来源，请参阅[安全：威胁模型](../../../security/10-lifecycle/)。

上面描述的最大威胁模型，也正是 Isolation 模式在设计时主要考虑的：开发期威胁。不仅许多前端构建期工具包含几十（甚至上百）个常常层层嵌套的依赖，一个复杂的应用还可能把大量（同样常常层层嵌套的）依赖打包进最终产物。

## 何时使用

只要能用，Tauri 就强烈建议使用 isolation 模式。由于 Isolation 应用会拦截来自前端的_**所有**_消息，它_始终_可用。

Tauri 也强烈建议：在使用任何外部 Tauri API 时都要锁定你的应用。作为开发者，你可以利用安全的 Isolation 应用来尝试验证 IPC 输入，确保它们处于预期的参数范围内。例如，你可能想检查读写文件的调用是否试图访问应用预期位置之外的路径。另一个例子是确保某个 Tauri API 的 HTTP fetch 调用只把 Origin 头设置为你应用期望的值。

话虽如此，由于它会拦截来自前端的_**所有**_消息，因此它对 [Events](https://tauri.app/reference/javascript/api/namespaceevent/) 这类常开 API 同样有效。由于某些事件可能让你自己的 rust 代码执行操作，也可以用同样的验证手段来处理它们。

## 如何工作

Isolation 模式的要点是在前端与 Tauri 核心之间注入一个安全应用，以拦截并修改传入的 IPC 消息。它利用 `<iframe>` 的沙箱特性，让这段 JavaScript 与主前端应用一起安全地运行。Tauri 在加载页面时强制执行 Isolation 模式，强制把所有发往 Tauri 核心的 IPC 调用先经由沙箱化的 Isolation 应用转发。当消息准备好传给 Tauri 核心时，会使用浏览器的 [SubtleCrypto](https://developer.mozilla.org/en-US/docs/Web/API/SubtleCrypto) 实现加密，再回传给主前端应用。到了那里，消息会被直接传给 Tauri 核心，随后像平常一样被解密和读取。

为了确保别人无法手动读取你应用某个特定版本的密钥并用它修改加密后的消息，每次应用运行时都会生成新的密钥。

### IPC 消息的大致步骤

为便于理解，下面按顺序列出了使用 Isolation 模式时，一条 IPC 消息发往 Tauri 核心所经历的大致步骤：

1. Tauri 的 IPC 处理器收到一条消息
2. IPC 处理器 -> Isolation 应用
3. `[sandbox]` Isolation 应用的 hook 运行，并可能修改消息
4. `[sandbox]` 使用运行时生成的密钥，以 AES-GCM 加密消息
5. `[encrypted]` Isolation 应用 -> IPC 处理器
6. `[encrypted]` IPC 处理器 -> Tauri 核心

_注意：箭头（->）表示消息传递。_

### 性能影响

由于确实会对消息加密，因此与 [Brownfield 模式](../2-brownfieldpattern/)相比会有额外开销，即使那个安全的 Isolation 应用什么都不做。除了对性能敏感的应用（它们通常小心翼翼地维护着少量依赖，以保证性能足够）之外，大多数应用不会注意到加解密 IPC 消息的运行时开销，因为消息相对较小，而 AES-GCM 相对较快。如果你不熟悉 AES-GCM，在这个语境下只需要知道：它是 [SubtleCrypto](https://developer.mozilla.org/en-US/docs/Web/API/SubtleCrypto) 中唯一包含的认证加密模式算法，而且你很可能每天都在 [TLS](https://en.wikipedia.org/wiki/Transport_Layer_Security) 的底层用到它。

此外，每次启动 Tauri 应用时还会生成一次密码学安全的密钥。如果系统已有足够的熵可以立即返回足够的随机数，一般不会察觉；这在桌面环境中极为常见。如果在无头环境中执行某些 [WebDriver 集成测试](../../../develop/tests/webdriver/1-overview/)，而你的操作系统又没有内置熵生成服务，那么你可能需要安装) `haveged` 之类的服务。<sup>Linux 5.6（2020 年 3 月）已包含使用推测执行生成熵的能力。</sup>

### 限制

平台差异导致 Isolation 模式存在一些限制。最显著的限制来自 Windows 上沙箱化 `<iframe>` 中外部文件无法正确加载。因此，我们在构建期实现了一个简单的脚本内联步骤：把相对于 Isolation 应用的脚本内容取出来并内联注入。这意味着像 `<script src="index.js"></script>` 这样典型的打包或简单包含文件仍然可用，但 ES Modules 之类较新的机制将_无法_成功加载。

## 建议

由于 Isolation 应用的意义在于防御开发期威胁，我们强烈建议让它尽可能简单。你不仅应尽量让 Isolation 应用的依赖保持最少，还应考虑让它所需的构建步骤也尽量少。这样你就不必在前端应用之外，还要担心 Isolation 应用遭受供应链攻击。

## 创建 Isolation 应用

在这个示例中，我们将做一个小的 hello-world 风格 Isolation 应用，并把它接到一个假想的现有 Tauri 应用上。它不会对经过它的消息做任何校验，只是把内容打印到 WebView 控制台。

为了举例，假设我们与 `tauri.conf.json` 处于同一目录。现有 Tauri 应用把 `frontendDist` 设为 `../dist`。

`../dist-isolation/index.html`：

```html
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <title>Isolation Secure Script</title>
  </head>
  <body>
    <script src="index.js"></script>
  </body>
</html>
```

`../dist-isolation/index.js`：

```javascript
window.__TAURI_ISOLATION_HOOK__ = (payload) => {
  // 不做任何校验或修改，只打印 hook 收到的内容
  console.log('hook', payload);
  return payload;
};
```

现在，我们只需把 `tauri.conf.json` 的[配置](#配置)设为使用 Isolation 模式，就从 [Brownfield 模式](../2-brownfieldpattern/)引导到 Isolation 模式了。

## 配置

假设我们的主前端 `frontendDist` 设为 `../dist`，并且把 Isolation 应用输出到 `../dist-isolation`。

```json
{
  "build": {
    "frontendDist": "../dist"
  },
  "app": {
    "security": {
      "pattern": {
        "use": "isolation",
        "options": {
          "dir": "../dist-isolation"
        }
      }
    }
  }
}
```
