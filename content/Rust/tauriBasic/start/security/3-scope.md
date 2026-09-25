+++
title = "3 命令作用域"
date = 2026-09-25T21:31:08+08:00
weight = 3
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/security/scope/](https://tauri.app/security/scope/)

作用域（scope）是一种细粒度定义 Tauri 命令（不）允许行为的方式。

作用域分为 `allow`（允许）和 `deny`（拒绝）两类，其中 `deny` 始终优先于 `allow`。

作用域类型必须是某种可用 [`serde`](https://docs.rs/serde/latest/serde/) 序列化的类型。一般来说这些类型是插件特有的。对于在 Tauri 应用中实现的作用域命令，作用域类型需要在应用中定义，然后在命令实现中强制执行。

例如，[`Fs`](https://github.com/tauri-apps/plugins-workspace/tree/v2/plugins/fs) 插件允许你用作用域来允许或拒绝特定目录和文件，而 [`http`](https://github.com/tauri-apps/plugins-workspace/tree/v2/plugins/http) 插件用作用域来过滤允许访问的 URL。

作用域会被传给命令，如何处理或正确强制执行由命令自身实现。

{{% alert title="警告" color="warning" %}}

命令开发者需要确保不存在可以绕过作用域的可能。作用域校验的实现应当经过审计以确保正确性。

{{% /alert %}}

## 示例

这些示例取自 [`Fs`](https://github.com/tauri-apps/plugins-workspace/tree/v2/plugins/fs) 插件的权限：

该插件中所有命令的作用域类型都是字符串，其中包含一个与 [`glob`](https://docs.rs/glob/latest/glob/) 兼容的路径。

```toml
identifier = "scope-applocaldata-recursive"
description = '''
This scope recursive access to the complete `$APPLOCALDATA` folder,
including sub directories and files.
'''

[[permission.scope.allow]]
path = "$APPLOCALDATA/**"
```

```toml
identifier = "deny-webview-data-linux"
description = '''
This denies read access to the
`$APPLOCALDATA` folder on linux as the webview data and
configuration values are stored here.
Allowing access can lead to sensitive information disclosure and
should be well considered.
'''
platforms = ["linux"]

[[permission.scope.deny]]
path = "$APPLOCALDATA/**"

[[permission]]
identifier = "deny-webview-data-windows"
description = '''
This denies read access to the
`$APPLOCALDATA/EBWebView` folder on windows as the webview data and
configuration values are stored here.
Allowing access can lead to sensitive information disclosure and
should be well considered.
'''
platforms = ["windows"]

[[permission.scope.deny]]
path = "$APPLOCALDATA/EBWebView/**"
```

上面的作用域可以用来允许访问 `APPLOCALDATA` 文件夹，同时阻止访问 Windows 上包含敏感 webview 数据的 `EBWebView` 子文件夹。

这些作用域可以合并成一个集合，从而减少重复配置，也让查看应用配置的人更容易理解。

首先把拒绝作用域合并为 `deny-default`：

```toml
identifier = "deny-default"
description = '''
This denies access to dangerous Tauri relevant files and
folders by default.
'''
permissions = ["deny-webview-data-linux", "deny-webview-data-windows"]
```

随后合并拒绝与允许作用域：

```toml
identifier = "scope-applocaldata-reasonable"
description = '''
This scope set allows access to the `APPLOCALDATA` folder and
subfolders except for linux,
while it denies access to dangerous Tauri relevant files and
folders by default on windows.
'''
permissions = ["scope-applocaldata-recursive", "deny-default"]
```

这些作用域既可以与插件的全局作用域一起扩展、用于所有命令，也可以在权限中与某个已启用的命令组合，只用于选定的命令。

对 `APPLOCALDATA` 中文件的合理只读访问可以写成这样：

```toml
identifier = "read-files-applocaldata"
description = '''
This set allows file read access to the `APPLOCALDATA` folder and
subfolders except for linux,
while it denies access to dangerous Tauri relevant files and
folders by default on windows.'''
permissions = ["scope-applocaldata-reasonable", "allow-read-file"]
```

这些示例只是展示作用域功能本身。每个插件或应用开发者都需要根据自己的使用场景，考虑合理的作用域组合。
