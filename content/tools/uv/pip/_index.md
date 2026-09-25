+++
title = "4 pip 接口"
date = 2026-09-25T19:02:24+08:00
weight = 4
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://docs.astral.sh/uv/pip/](https://docs.astral.sh/uv/pip/)

# 4 pip 接口

uv 为常用的 `pip`、`pip-tools` 和 `virtualenv` 命令提供了可直接替换的实现。这些命令直接作用于虚拟环境，而 uv 的主要接口则自动管理虚拟环境。`uv pip` 接口把 uv 的速度与功能带给高级用户，以及尚未准备从 `pip` 和 `pip-tools` 迁移的项目。

以下章节讨论使用 `uv pip` 的基础知识：

- [创建和使用环境](./4.1-environments/)
- [安装和管理包](./4.2-packages/)
- [检查环境和包](./4.3-inspection/)
- [声明包依赖](./4.4-dependencies/)
- [锁定和同步环境](./4.5-compile/)

请注意，这些命令并*不*完全实现它们所参照工具的接口和行为。你越偏离常见工作流，就越可能遇到差异。细节请参阅 [pip 兼容性指南](./4.6-compatibility/)。

> **重要**
>
> uv 不依赖也不调用 pip。pip 接口之所以这样命名，是为了突出它专门提供与 pip 接口一致的低层命令，并把它与 uv 其他更高抽象层次的命令区分开来。
