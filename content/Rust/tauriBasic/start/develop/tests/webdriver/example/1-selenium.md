+++
title = "1 Selenium"
date = 2026-09-25T21:31:08+08:00
weight = 1
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/develop/tests/webdriver/example/selenium/](https://tauri.app/develop/tests/webdriver/example/selenium/)

{{% alert title="注意" %}}

请务必先阅读[前置条件说明](../../2-manualsetup/)，才能跟随本指南操作。

{{% /alert %}}

这个 WebDriver 测试示例将使用 [Selenium](https://selenium.dev/) 和一个流行的 Node.js 测试套件。我们假设你已经安装了
Node.js，以及 `npm` 或 `yarn`，尽管[完成的示例项目](https://github.com/tauri-apps/webdriver-example)使用的是 `pnpm`。

## 为测试创建目录

让我们在项目中为编写这些测试开辟空间。这个示例项目我们会用一个嵌套目录，因为后面还会介绍其它框架，但通常你只需要用其中一个。用 `mkdir -p e2e-tests` 创建我们将使用的目录。本指南余下部分假定你位于
`e2e-tests` 目录中。

## 初始化 Selenium 项目

我们将使用一个现成的 `package.json` 来引导这个测试套件，因为我们已经选定了具体要用的依赖，并希望展示一个简单可用的方案。本节末尾有一个折叠的
从零开始配置指南。

`package.json`：

```json
{
  "name": "selenium",
  "version": "1.0.0",
  "private": true,
  "type": "module",
  "scripts": {
    "test": "mocha"
  },
  "dependencies": {
    "chai": "^5.2.1",
    "mocha": "^11.7.1",
    "selenium-webdriver": "^4.34.0"
  }
}
```

我们有一个以 `test` 命令暴露的脚本，用于运行 [Mocha](https://mochajs.org/) 测试框架。我们还用到若干依赖来运行测试：
[Mocha](https://mochajs.org/) 作为测试框架，[Chai](https://www.chaijs.com/) 作为断言库，以及
[`selenium-webdriver`](https://www.npmx.dev/package/selenium-webdriver)，也就是 Node.js 的 [Selenium](https://selenium.dev/) 包。

<details>
  <summary>如果你想看如何从零开始搭建项目，请点我</summary>

如果你想从零安装这些依赖，只需运行以下命令。

**包管理器**

{{< tabpane text=true persist=disabled >}}
{{% tab header="npm" %}}

```sh
npm install mocha chai selenium-webdriver
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn add mocha chai selenium-webdriver
```

{{% /tab %}}

{{< /tabpane >}}
我还建议在 `package.json` 的 `"scripts"` 键中加入 `"test": "mocha"` 项，这样运行 Mocha 只需简单地调用：

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
</details>

## 测试

与 [WebdriverIO 测试套件](../2-webdriverio/#配置)不同，Selenium 开箱并不自带测试套件，而是留给开发者自行构建。我们选择了
[Mocha](https://mochajs.org/)，它相当中立且与 WebDriver 无关，因此我们的脚本需要做一些工作来按正确顺序设置好一切。[Mocha](https://mochajs.org/) 默认期望在 `test/test.js` 处有一个测试文件，所以我们现在就创建它。

`test/test.js`：

```javascript
import path from 'path';
import { expect } from 'chai';
import { spawn, spawnSync } from 'child_process';
import { Builder, By, Capabilities } from 'selenium-webdriver';
import { fileURLToPath } from 'url';

const __dirname = fileURLToPath(new URL('.', import.meta.url));

// 创建指向预期应用二进制文件的路径
const application = path.resolve(
  __dirname,
  '..',
  '..',
  'src-tauri',
  'target',
  'debug',
  'tauri-app'
);

// 跟踪我们创建的 webdriver 实例
let driver;

// 跟踪我们启动的 tauri-driver 进程
let tauriDriver;
let exit = false;

before(async function () {
  // 把超时设为 2 分钟，以便程序在需要时完成构建
  this.timeout(120000);

  // 确保应用已经构建
  spawnSync('yarn', ['tauri', 'build', '--debug', '--no-bundle'], {
    cwd: path.resolve(__dirname, '../..'),
    stdio: 'inherit',
    shell: true,
  });

  // 启动 tauri-driver
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

  const capabilities = new Capabilities();
  capabilities.set('tauri:options', { application });
  capabilities.setBrowserName('wry');

  // 启动 webdriver 客户端
  driver = await new Builder()
    .withCapabilities(capabilities)
    .usingServer('http://127.0.0.1:4444/')
    .build();
});

after(async function () {
  // 停止 webdriver 会话
  await closeTauriDriver();
});

describe('Hello Tauri', () => {
  it('should be cordial', async () => {
    const text = await driver.findElement(By.css('body > h1')).getText();
    expect(text).to.match(/^[hH]ello/);
  });

  it('should be excited', async () => {
    const text = await driver.findElement(By.css('body > h1')).getText();
    expect(text).to.match(/!$/);
  });

  it('should be easy on the eyes', async () => {
    // selenium 会把颜色的 css 值返回为 rgb(r, g, b)
    const text = await driver
      .findElement(By.css('body'))
      .getCssValue('background-color');

    const rgb = text.match(/^rgb\((?<r>\d+), (?<g>\d+), (?<b>\d+)\)$/).groups;
    expect(rgb).to.have.all.keys('r', 'g', 'b');

    const luma = 0.2126 * rgb.r + 0.7152 * rgb.g + 0.0722 * rgb.b;
    expect(luma).to.be.lessThan(100);
  });
});

async function closeTauriDriver() {
  exit = true;
  // 结束 tauri-driver 进程
  tauriDriver.kill();
  // 停止 webdriver 会话
  await driver.quit();
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

onShutdown(() => {
  closeTauriDriver();
});
```

如果你熟悉 JS 测试框架，`describe`、`it` 和 `expect` 应该看起来很眼熟。我们还有略复杂的 `before()` 和 `after()` 回调来设置和拆除 mocha。非测试本身的代码行都有注释说明设置与拆除逻辑。如果你熟悉
[WebdriverIO 示例](../2-webdriverio/#spec)中的 Spec 文件，你会发现这里多出很多不是测试的代码，因为我们需要额外设置一些
WebDriver 相关的东西。

## 运行测试套件

现在依赖和测试脚本都配置好了，让我们运行它！

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
$ Mocha


  Hello Tauri
    ✔ should be cordial (120ms)
    ✔ should be excited
    ✔ should be easy on the eyes


  3 passing (588ms)

Done in 0.93s.
```

可以看到，我们用 `describe` 创建的 `Hello Tauri` 测试套件中，用 `it` 创建的 3 个测试项全部通过了！

借助 [Selenium](https://selenium.dev/) 和与测试套件的一些连接，我们就在完全没有修改 Tauri 应用的情况下启用了端到端测试！
