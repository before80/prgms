+++
title = "2 Mock Tauri API"
date = 2026-09-25T21:31:08+08:00
weight = 2
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/develop/tests/mocking/](https://tauri.app/develop/tests/mocking/)

在编写前端测试时，通常需要一个“假的” Tauri 环境来模拟窗口或拦截 IPC 调用，也就是所谓的_模拟（mocking）_。
[`@tauri-apps/api/mocks`](https://tauri.app/reference/javascript/api/namespacemocks/) 模块提供了一些实用工具，让它对你来说更简单：

{{% alert title="警告" color="warning" %}}

记得在每次测试运行后清理 mock，以撤销 mock 状态在多次运行之间的变更！更多信息见 [`clearMocks()`](https://tauri.app/reference/javascript/api/namespacemocks/#clearmocks) 文档。

{{% /alert %}}

## IPC 请求

最常见的是你想拦截 IPC 请求；这在多种场景下都很有用：

- 确保发起了正确的后端调用
- 模拟后端函数返回不同的结果

Tauri 提供了 mockIPC 函数来拦截 IPC 请求。你可以在[这里](https://tauri.app/reference/javascript/api/namespacemocks/#mockipc)找到关于该具体 API 的更多细节。

{{% alert title="注意" %}}

下面的示例使用 [Vitest](https://vitest.dev)，但你也可以使用 jest 等任何其它前端测试库。

{{% /alert %}}

### 为 `invoke` 模拟命令

```javascript
import { beforeAll, expect, test } from "vitest";
import { randomFillSync } from "crypto";

import { mockIPC } from "@tauri-apps/api/mocks";
import { invoke } from "@tauri-apps/api/core";

// jsdom 不带 WebCrypto 实现
beforeAll(() => {
  Object.defineProperty(window, 'crypto', {
    value: {
      // @ts-ignore
      getRandomValues: (buffer) => {
        return randomFillSync(buffer);
      },
    },
  });
});


test("invoke simple", async () => {
  mockIPC((cmd, args) => {
    // 模拟一个名为 "add" 的 rust 命令，只把两个数相加
    if(cmd === "add") {
      return (args.a as number) + (args.b as number);
    }
  });
});
```

有时你想跟踪一次 IPC 调用的更多信息：该命令被调用了多少次？到底有没有被调用？
你可以把 [`mockIPC()`](https://tauri.app/reference/javascript/api/namespacemocks/#mockipc) 与其它监视和模拟工具一起使用来测试：

```javascript
import { beforeAll, expect, test, vi } from "vitest";
import { randomFillSync } from "crypto";

import { mockIPC } from "@tauri-apps/api/mocks";
import { invoke } from "@tauri-apps/api/core";

// jsdom 不带 WebCrypto 实现
beforeAll(() => {
  Object.defineProperty(window, 'crypto', {
    value: {
      // @ts-ignore
      getRandomValues: (buffer) => {
        return randomFillSync(buffer);
      },
    },
  });
});


test("invoke", async () => {
  mockIPC((cmd, args) => {
    // 模拟一个名为 "add" 的 rust 命令，只把两个数相加
    if(cmd === "add") {
      return (args.a as number) + (args.b as number);
    }
  });

  // 我们可以使用 vitest 提供的监视工具来跟踪被模拟的函数
  const spy = vi.spyOn(window.__TAURI_INTERNALS__, "invoke");

  expect(invoke("add", { a: 12, b: 15 })).resolves.toBe(27);
  expect(spy).toHaveBeenCalled();
});
```

要模拟对 sidecar 或 shell 命令的 IPC 请求，你需要在调用 `spawn()` 或 `execute()` 时取得事件处理器的 ID，并用这个 ID 发出后端会回传的事件：

```javascript
mockIPC(async (cmd, args) => {
  if (args.message.cmd === 'execute') {
    const eventCallbackId = `_${args.message.onEventFn}`;
    const eventEmitter = window[eventCallbackId];

    // 'Stdout' 事件可以被多次调用
    eventEmitter({
      event: 'Stdout',
      payload: 'some data sent from the process',
    });

    // 'Terminated' 事件必须在最后调用，以兑现 promise
    eventEmitter({
      event: 'Terminated',
      payload: {
        code: 0,
        signal: 'kill',
      },
    });
  }
});
```

{{% alert title="另见" %}}

`mockIPC` 在 mock 运行时下伪造 `invoke`——不会运行真实的 webview 或 Rust 后端。要在**端到端**测试中针对运行中的应用或浏览器中的前端模拟同样的命令，
[`@wdio/tauri-service`](https://webdriver.io/docs/desktop-testing/tauri) 提供了等价的 `browser.tauri.mock()`。请参阅 [WebDriver 测试](../webdriver/1-overview/)。

{{% /alert %}}

### 模拟事件

*需要 2.7.0 或更高版本。*

通过 `shouldMockEvents` 选项，可以部分支持用[事件系统](../../4-callingfrontend/#事件系统)模拟 Rust 代码发出的事件：

```javascript
import { mockIPC, clearMocks } from '@tauri-apps/api/mocks';
import { emit, listen } from '@tauri-apps/api/event';
import { afterEach, expect, test, vi } from 'vitest';

test('mocked event', () => {
  mockIPC(() => {}, { shouldMockEvents: true }); // 启用事件模拟

  const eventHandler = vi.fn();
  listen('test-event', eventHandler);

  emit('test-event', { foo: 'bar' });
  expect(eventHandler).toHaveBeenCalledWith({
    event: 'test-event',
    payload: { foo: 'bar' },
  });
});
```

`emitTo` 和 `emit_filter` 目前**不**支持。

## 窗口

有时你有窗口特定的代码（例如启动画面窗口），因此需要模拟不同的窗口。
你可以用 [`mockWindows()`](https://tauri.app/reference/javascript/api/namespacemocks/#mockwindows) 方法创建假的窗口标签。第一个字符串标识“当前”窗口（也就是你的 JavaScript 认为自己所在的窗口），其它所有字符串都被视为额外窗口。

{{% alert title="注意" %}}

[`mockWindows()`](https://tauri.app/reference/javascript/api/namespacemocks/#mockwindows) 只伪造窗口的存在，不伪造窗口属性。要模拟窗口属性，你需要用 [`mockIPC()`](https://tauri.app/reference/javascript/api/namespacemocks/#mockipc) 拦截相应的调用。

{{% /alert %}}

```javascript
import { beforeAll, expect, test } from 'vitest';
import { randomFillSync } from 'crypto';

import { mockWindows } from '@tauri-apps/api/mocks';

// jsdom 不带 WebCrypto 实现
beforeAll(() => {
  Object.defineProperty(window, 'crypto', {
    value: {
      // @ts-ignore
      getRandomValues: (buffer) => {
        return randomFillSync(buffer);
      },
    },
  });
});

test('invoke', async () => {
  mockWindows('main', 'second', 'third');

  const { getCurrent, getAll } = await import('@tauri-apps/api/webviewWindow');

  expect(getCurrent()).toHaveProperty('label', 'main');
  expect(getAll().map((w) => w.label)).toEqual(['main', 'second', 'third']);
});
```
