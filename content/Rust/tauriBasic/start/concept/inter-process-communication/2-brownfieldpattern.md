+++
title = "2 Brownfield 模式"
date = 2026-09-25T21:31:08+08:00
weight = 2
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/concept/inter-process-communication/brownfield/](https://tauri.app/concept/inter-process-communication/brownfield/)

_**这是默认模式。**_

这是使用 Tauri 最简单、最直接的模式，因为它尽可能兼容现有的前端项目。简而言之，它尽量不要求现有 Web 前端在浏览器中使用之外的东西。
但并非在现有浏览器应用中能工作的_**所有东西**_都能开箱即用。

如果你对 Brownfield 软件开发整体不太熟悉，[Brownfield 的维基百科条目](https://en.wikipedia.org/wiki/Brownfield_(software_development))给出了不错的概述。对 Tauri 来说，这里的“既有软件”指的是当前浏览器的支持情况与行为，而不是遗留系统。

## 配置

由于 Brownfield 模式是默认模式，它不需要设置任何配置项。若想显式地设置它，你可以在 `tauri.conf.json` 配置文件中使用 `app > security > pattern` 对象。

```json
{
  "app": {
    "security": {
      "pattern": {
        "use": "brownfield"
      }
    }
  }
}
```

_**brownfield 模式没有额外的配置选项。**_
