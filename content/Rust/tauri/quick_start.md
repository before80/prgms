+++
title = "quick_start"
date = 2026-05-26T09:38:56+08:00
weight = 1
type = "docs"
description = ""
isCJKLanguage = true
draft = false

+++



## 使用 tauri的步骤

​	`cargo install` 专门用来安装二进制 crate（提供可执行程序），而不是库 crate（库 crate 通常通过 Cargo.toml 的 `[dependencies]` 引入）.

​	`create-tauri-app` 是 Tauri 官方提供的脚手架工具，用来快速初始化一个 Tauri 项目, 类似于 `create-react-app` 或 `npm create vite`，它会引导你选择前端框架、包管理器等，然后自动生成项目目录和基础文件，让你跳过手动配置的步骤.

​	`--locked` 标志确保安装过程的依赖版本与工具发布时完全一致. 正常情况下，`cargo install` 会忽略被安装 crate 源码中自带的 `Cargo.lock` 文件，转而在你本地重新生成一个最新的锁文件，解析依赖时可能拉取到与工具不兼容的新版依赖。加上 `--locked` 后，Cargo 会强制使用 crate 仓库里已有的 `Cargo.lock` 文件来解析依赖，相当于将依赖版本“冻结”在工具发布时经过测试的那一组版本上。

​	安装后的可执行文件默认放在 `$HOME/.cargo/bin/`（Linux/macOS）, 或 `%USERPROFILE%\.cargo\bin\`（Windows）目录下，只要这个目录在系统的 `PATH` 环境变量中，你就可以直接在终端调用该命令

```sh
cargo install create-tauri-app --locked
```

使用 create-tauri-app

```sh
cargo create-tauri-app
```

例如, 以下使用 `tauri_app1` 作为 `project name`

```powershell
(base) PS E:\dev\RustPrjs\tauri_demo1> cargo create-tauri-app
✔ Project name · tauri_app1
✔ Identifier · com.hellome.tauri_app1
✔ Choose which language to use for your frontend · Rust - (cargo)
✔ Choose your UI template · Dioxus - (https://dioxuslabs.com/)

Template created!

Your system is missing dependencies (or they do not exist in $PATH):
╭────────────┬─────────────────────────────────────────╮
│ Dioxus CLI │ Run `cargo install dioxus-cli --locked` │
╰────────────┴─────────────────────────────────────────╯

Make sure you have installed the prerequisites for your OS: https://tauri.app/start/prerequisites/, then run:
  cd tauri_app1
  cargo tauri android init

For Desktop development, run:
  cargo tauri dev

For Android development, run:
  cargo tauri android dev
```





安装 cargo-binstall（如果还没装）

```sh
cargo install cargo-binstall
```

从源码编译 `dioxus-cli` 时会出现依赖冲突问题, 故用 binstall 安装预编译的 `dioxus-cli`.

```sh
cargo binstall dioxus-cli --force
```

验证dioxus-cli是否已经安装

```sh
dx --version
```



切换到  `tauri_app1` 目录

```sh
cd tauri_app1
```



启动开发服务器

```sh
 cargo tauri dev
```

