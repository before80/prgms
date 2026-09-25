+++
title = "2 权限"
date = 2026-09-25T21:31:08+08:00
weight = 2
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/security/permissions/](https://tauri.app/security/permissions/)

权限（Permission）描述了命令所拥有的明确特权。

```toml
identifier = "my-identifier"
description = "This describes the impact and more."
commands.allow = [
    "read_file"
]

[[permission.scope.allow]]
my-scope = "$HOME/*"

[[permission.scope.deny]]
my-scope = "$HOME/secret"
```

它可以让命令能够在 Tauri 应用的前端被访问，也可以把作用域映射到命令，并定义哪些命令被启用。权限可以启用或拒绝某些命令、定义作用域，或者两者结合。

要把某个权限授予或拒绝给应用的窗口或 webview，你必须在[能力](../4-capabilities/)中引用该权限。

权限可以组合成一个集合，挂在一个新的标识符下。这称为权限集（permission set）。它让你可以把与作用域相关的权限和与命令相关的权限组合起来，也可以把操作系统特有的权限归组或打包成更好用的集合。

作为插件开发者，你可以为自己暴露的所有命令提供多个预定义、命名良好的权限。

作为应用开发者，你可以扩展已有插件的权限，或为自己的命令定义权限。它们可以被归组或扩展成一个集合，以便复用或简化后续的主配置文件。

## 权限标识符

权限标识符用于确保权限可被复用且名称唯一。

{{% alert title="提示" %}}

这里的 **name** 指插件 crate 名称去掉 `tauri-plugin-` 前缀后的部分。这样命名空间化是为了降低命名冲突的可能性。引用应用自身的权限时则不需要。

{{% /alert %}}

- `<name>:default` 表示该权限是某个插件或应用的默认权限
- `<name>:<command-name>` 表示该权限针对单个命令

插件前缀 `tauri-plugin-` 会在编译期自动添加到插件的标识符前面，无需手动指定。

标识符仅限于 ASCII 小写字母 `[a-z]`，且标识符的最大长度目前限制为 `116`，这源于以下常量：

```rust
const PLUGIN_PREFIX: &str = "tauri-plugin-";

// https://doc.rust-lang.org/cargo/reference/manifest.html#the-name-field
const MAX_LEN_PREFIX: usize = 64 - PLUGIN_PREFIX.len();
const MAX_LEN_BASE: usize = 64;
const MAX_LEN_IDENTIFIER: usize = MAX_LEN_PREFIX + 1 + MAX_LEN_BASE;
```

## 配置文件

一个示例 Tauri **插件**目录结构的简化版本：

```sh
├── README.md
├── src
│  └── lib.rs
├── build.rs
├── Cargo.toml
├── permissions
│  └── <identifier>.json/toml
│  └── default.json/toml
```

默认权限以特殊方式处理：只要使用 Tauri CLI 向 Tauri 应用添加插件，它就会被自动加入应用配置。

对**应用**开发者来说，结构是类似的：

```sh
├── index.html
├── package.json
├── src
├── src-tauri
│   ├── Cargo.toml
│   ├── permissions
│      └── <identifier>.toml
|   ├── capabilities
│      └── <identifier>.json/.toml
│   ├── src
│   ├── tauri.conf.json
```

{{% alert title="注意" %}}

作为应用开发者，能力（capability）文件可以用 `json`/`json5` 或 `toml` 编写，而权限只能用 `toml` 定义。

{{% /alert %}}

## 示例

来自 `File System` 插件的示例权限。

```toml
identifier = "scope-home"
description = """This scope permits access to all files and
list content of top level directories in the `$HOME`folder."""

[[permission.scope.allow]]
path = "$HOME/*"
```

```toml
identifier = "read-files"
description = """This enables all file read related
commands without any pre-configured accessible paths."""
commands.allow = [
    "read_file",
    "read",
    "open",
    "read_text_file",
    "read_text_file_lines",
    "read_text_file_lines_next"
]
```

```toml
identifier = "allow-mkdir"
description = "This enables the mkdir command."
commands.allow = [
    "mkdir"
]
```

在你的应用中扩展上述插件权限的示例实现：

```toml
identifier = "allow-home-read-extended"
description = """ This allows non-recursive read access to files and to create directories
in the `$HOME` folder.
"""
permissions = [
    "fs:read-files",
    "fs:scope-home",
    "fs:allow-mkdir"
]
```
