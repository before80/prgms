+++
title = "2 WebdriverIO"
date = 2026-09-25T21:31:08+08:00
weight = 2
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/develop/tests/webdriver/example/webdriverio/](https://tauri.app/develop/tests/webdriver/example/webdriverio/)

{{% alert title="注意" %}}

请务必先阅读[前置条件说明](../../2-manualsetup/)，才能跟随本指南操作。

{{% /alert %}}

{{% alert title="正在使用 WebdriverIO 的 Tauri 服务？" %}}

本指南手工把 [WebdriverIO](https://webdriver.io/) 接到 [`tauri-driver`](https://crates.io/crates/tauri-driver) 上，以便你看清各部分如何配合。大多数项目应当改用
[`@wdio/tauri-service`](https://webdriver.io/docs/desktop-testing/tauri)，它把这一切自动化并支持 macOS——参见
[WebDriver 概述](../../1-overview/)。

{{% /alert %}}

这个 WebDriver 测试示例将使用 [WebdriverIO](https://webdriver.io/) 及其测试套件。我们假设你已经安装了 Node.js，以及 `npm` 或 `yarn`，尽管[完成的示例项目](https://github.com/tauri-apps/webdriver-example)使用的是 `pnpm`。

## 为测试创建目录

让我们在项目中为编写这些测试开辟空间。这个示例项目我们会用一个嵌套目录，因为后面还会介绍其它框架，但通常你只需要用其中一个。用 `mkdir e2e-tests` 创建我们将使用的目录。本指南余下部分假定你位于
`e2e-tests` 目录中。

## 初始化 WebdriverIO 项目

我们将使用一个现成的 `package.json` 来引导这个测试套件，因为我们已经选定了具体的
[WebdriverIO](https://webdriver.io/) 配置项，并希望展示一个简单可用的方案。本节末尾有一个折叠的从零开始配置指南。

`package.json`：

```json
{
  "name": "webdriverio",
  "version": "1.0.0",
  "private": true,
  "type": "module",
  "scripts": {
    "test": "wdio run wdio.conf.js"
  },
  "dependencies": {
    "@wdio/cli": "^9.19.0"
  },
  "devDependencies": {
    "@wdio/local-runner": "^9.19.0",
    "@wdio/mocha-framework": "^9.19.0",
    "@wdio/spec-reporter": "^9.19.0"
  }
}
```

我们有一个以 `test` 命令暴露的脚本，用于把某个 [WebdriverIO](https://webdriver.io/) 配置作为测试套件运行。我们还用到了最初设置时由
`@wdio/cli` 命令添加的若干依赖。简而言之，这些依赖用于最简单的本地 WebDriver 运行器配置，以 [Mocha](https://mochajs.org/) 作为测试框架，并使用简单的 Spec Reporter。

<details>
  <summary>如果你想看如何从零开始搭建项目，请点我</summary>

该 CLI 是交互式的，你可以自行选择要使用的工具。注意你可能会与本指南余下部分产生分歧，需要自己处理这些差异。

让我们把 [WebdriverIO](https://webdriver.io/) CLI 加入这个 npm 项目。

**包管理器**

{{< tabpane text=true persist=disabled >}}
{{% tab header="npm" %}}

```sh
npm install @wdio/cli
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn add @wdio/cli
```

{{% /tab %}}

{{< /tabpane >}}
然后运行交互式配置命令来设置 [WebdriverIO](https://webdriver.io/) 测试套件：

**包管理器**

{{< tabpane text=true persist=disabled >}}
{{% tab header="npm" %}}

```sh
npx wdio config
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn wdio config
```

{{% /tab %}}

{{< /tabpane >}}
</details>

## 配置

你可能注意到 `package.json` 中的 `test` 脚本提到了 `wdio.conf.js` 文件。那就是 [WebdriverIO](https://webdriver.io/)
配置文件，它控制我们测试套件的大部分行为。

`wdio.conf.js`：

```javascript
import path from 'path';
import { spawn, spawnSync } from 'child_process';
import { fileURLToPath } from 'url';

const __dirname = fileURLToPath(new URL('.', import.meta.url));

// 跟踪 `tauri-driver` 子进程
let tauriDriver;
let exit = false;

export const config = {
  host: '127.0.0.1',
  port: 4444,
  specs: ['./develop/tests/specs/**/*.js'],
  maxInstances: 1,
  capabilities: [
    {
      maxInstances: 1,
      'tauri:options': {
        application: '../src-tauri/target/debug/tauri-app',
      },
    },
  ],
  reporters: ['spec'],
  framework: 'mocha',
  mochaOpts: {
    ui: 'bdd',
    timeout: 60000,
  },

  // 确保 rust 项目已经构建，因为 webdriver 会话期望该二进制文件存在
  onPrepare: () => {
    // 如果你不使用 npm，请去掉多余的 `--`！
    spawnSync(
      'npm',
      ['run', 'tauri', 'build', '--', '--debug', '--no-bundle'],
      {
        cwd: path.resolve(__dirname, '..'),
        stdio: 'inherit',
        shell: true,
      }
    );
  },

  // 确保在会话开始之前运行 `tauri-driver`，这样我们才能代理 webdriver 请求
  beforeSession: () => {
    tauriDriver = spawn(
      path.resolve(os.homedir(), '.cargo', 'bin', 'tauri-driver'),
      [],
      { stdio: [null, process.stdout, process.stderr] }
    );

    tauriDriver.on('error', (error) => {
      console.error('tauri-driver error:', error);
      process.exit(1);
    });
    tauriDriver.on('exit', (code) => {
      if (!exit) {
        console.error('tauri-driver exited with code:', code);
        process.exit(1);
      }
    });
  },

  // 清理我们在会话开始时启动的 `tauri-driver` 进程
  // 注意如果会话启动失败，afterSession 可能不会运行，因此我们也在关闭时执行清理
  afterSession: () => {
    closeTauriDriver();
  },
};

function closeTauriDriver() {
  exit = true;
  tauriDriver?.kill();
}

function onShutdown(fn) {
  const cleanup = () => {
    try {
      fn();
    } finally {
      process.exit();
    }
  };

  process.on('exit', cleanup);
  process.on('SIGINT', cleanup);
  process.on('SIGTERM', cleanup);
  process.on('SIGHUP', cleanup);
  process.on('SIGBREAK', cleanup);
}

// 确保我们的测试进程退出时关闭 tauri-driver
onShutdown(() => {
  closeTauriDriver();
});
```

如果你对 `config` 对象上的属性感兴趣，我们[建议阅读相关文档](https://webdriver.io/docs/configurationfile)。
对于非 WDIO 特有的条目，注释解释了为什么我们要在 `onPrepare`、`beforeSession` 和 `afterSession` 中运行命令。我们
还把 specs 设为 `"./test/specs/**/*.js"`，所以现在来创建一个 spec。

## Spec

Spec 包含测试你实际应用的代码。测试运行器会加载这些 spec，并按它认为合适的方式自动运行。现在就在我们指定的目录中创建 spec。

`test/specs/example.e2e.js`：

```javascript
function luma(hex) {
  if (hex.startsWith('#')) {
    hex = hex.substring(1);
  }

  const rgb = parseInt(hex, 16);
  const r = (rgb >> 16) & 0xff;
  const g = (rgb >> 8) & 0xff;
  const b = (rgb >> 0) & 0xff;
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}

describe('Hello Tauri', () => {
  it('should be cordial', async () => {
    const header = await $('body > h1');
    const text = await header.getText();
    expect(text).toMatch(/^[hH]ello/);
  });

  it('should be excited', async () => {
    const header = await $('body > h1');
    const text = await header.getText();
    expect(text).toMatch(/!$/);
  });

  it('should be easy on the eyes', async () => {
    const body = await $('body');
    const backgroundColor = await body.getCSSProperty('background-color');
    expect(luma(backgroundColor.parsed.hex)).toBeLessThan(100);
  });
});
```

顶部的 `luma` 函数只是一个供某个测试使用的辅助函数，与实际测试应用无关。如果你熟悉其它测试框架，可能会注意到
用到的 `describe`、`it` 和 `expect` 等相似的函数。其它 API，例如 `$` 及其暴露的方法，都记录在
[WebdriverIO API 文档](https://webdriver.io/docs/api)中。

## 运行测试套件

现在配置和 spec 都准备好了，让我们运行它！

**包管理器**

{{< tabpane text=true persist=disabled >}}
{{% tab header="npm" %}}

```sh
npm test
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn test
```

{{% /tab %}}

{{< /tabpane >}}
我们应当看到如下输出：

```text
yarn run v1.22.11
$ wdio run wdio.conf.js

Execution of 1 workers started at 2021-08-17T08:06:10.279Z

[0-0] RUNNING in undefined - /develop/tests/specs/example.e2e.js
[0-0] PASSED in undefined - /develop/tests/specs/example.e2e.js

 "spec" Reporter:
------------------------------------------------------------------
[wry 0.12.1 linux #0-0] Running: wry (v0.12.1) on linux
[wry 0.12.1 linux #0-0] Session ID: 81e0107b-4d38-4eed-9b10-ee80ca47bb83
[wry 0.12.1 linux #0-0]
[wry 0.12.1 linux #0-0] » /develop/tests/specs/example.e2e.js
[wry 0.12.1 linux #0-0] Hello Tauri
[wry 0.12.1 linux #0-0]    ✓ should be cordial
[wry 0.12.1 linux #0-0]    ✓ should be excited
[wry 0.12.1 linux #0-0]    ✓ should be easy on the eyes
[wry 0.12.1 linux #0-0]
[wry 0.12.1 linux #0-0] 3 passing (244ms)


Spec Files:	 1 passed, 1 total (100% completed) in 00:00:01

Done in 1.98s.
```

可以看到 Spec Reporter 告诉我们 `test/specs/example.e2e.js` 文件中的 3 个测试全部通过，以及最终报告
`Spec Files: 1 passed, 1 total (100% completed) in 00:00:01`。

使用 [WebdriverIO](https://webdriver.io/) 测试套件，我们只用几行配置和一个运行命令，就轻松为 Tauri 应用启用了端到端测试！更棒的是，我们完全不需要修改应用。
