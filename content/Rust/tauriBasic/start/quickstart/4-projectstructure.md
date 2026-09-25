+++
title = "4 项目结构"
date = 2026-09-25T21:31:08+08:00
weight = 4
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/start/project-structure/](https://tauri.app/start/project-structure/)

一个 Tauri 项目通常由两部分组成：一个 Rust 项目和一个 JavaScript 项目（可选），典型的目录结构大致如下：

```
.
├── package.json
├── index.html
├── src/
│   ├── main.js
├── src-tauri/
│   ├── Cargo.toml
│   ├── Cargo.lock
│   ├── build.rs
│   ├── tauri.conf.json
│   ├── src/
│   │   ├── main.rs
│   │   └── lib.rs
│   ├── icons/
│   │   ├── icon.png
│   │   ├── icon.icns
│   │   └── icon.ico
│   └── capabilities/
│       └── default.json
```

在这个例子中，JavaScript 项目位于顶层，Rust 项目位于 `src-tauri/` 内。该 Rust 项目是一个普通的 [Cargo 项目](https://doc.rust-lang.org/cargo/guide/project-layout.html)，只是多了一些额外的文件：

- `tauri.conf.json` 是 Tauri 的主配置文件，其中包含从应用标识符到开发服务器 URL 的所有内容。该文件也是 [Tauri CLI](../frontend-configuration/) 用来定位 Rust 项目的标记文件。若要进一步了解，请参阅 [Tauri 配置](../../develop/2-configurationfiles/#tauri-配置)。
- `capabilities/` 目录是 Tauri 默认读取[能力文件](../../security/4-capabilities/)的文件夹（简而言之，你需要在这里允许某些命令，才能在 JavaScript 代码中使用它们）。若要进一步了解，请参阅[安全](../../security/1-overview/)。
- `icons/` 目录是 [`tauri icon`](https://tauri.app/reference/cli/#icon) 命令的默认输出目录，通常在 `tauri.conf.json > bundle > icon` 中被引用，并用作应用的图标。
- `build.rs` 包含 `tauri_build::build()`，用于 Tauri 的构建系统。
- `src/lib.rs` 包含 Rust 代码和移动端入口点（即以 `#[cfg_attr(mobile, tauri::mobile_entry_point)]` 标记的函数）。我们不直接在 `main.rs` 中编写代码，是因为在移动端构建时会把你的应用编译成一个库，并通过平台框架加载它。
- `src/main.rs` 是桌面端的主入口点，我们在 `main` 中运行 `app_lib::run()`，以使用与移动端相同的入口点。因此为简单起见，请不要修改这个文件，而是修改 `lib.rs`。注意，`app_lib` 对应 Cargo.toml 中的 `[lib.name]`。

Tauri 的工作方式类似于静态 Web 托管：构建时会先把你的 JavaScript 项目编译成静态文件，然后编译 Rust 项目并把那些静态文件打包进去。因此 JavaScript 项目的配置方式与构建一个静态网站基本相同。若要进一步了解，请参阅[前端配置](../frontend-configuration/)。

如果你只想使用 Rust 代码，只需删除其它所有内容，并将 `src-tauri/` 文件夹作为顶层项目，或作为你的 Rust 工作区的一个成员。

## 后续步骤

- [添加并配置前端框架](../frontend-configuration/)
- [Tauri 命令行界面（CLI）参考](https://tauri.app/reference/cli/)
- [学习如何开发你的 Tauri 应用](../../develop/1-overview/)
- [探索更多扩展 Tauri 的功能](../../plugin/1-overview/)
